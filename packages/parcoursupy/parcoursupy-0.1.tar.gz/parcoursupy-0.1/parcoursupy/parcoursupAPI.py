import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
import json
import re
import random
import string
import time
import locale

parcoursup_url = "https://dossier.parcoursup.fr/Candidat/"
parcoursup_mobile = "https://mobile.parcoursup.fr/NotificationsService/services/"
JSON_HEADERS = {"Content-Type": "application/json"}

locale.setlocale(locale.LC_ALL, 'fr_FR')


class Parcoursup_Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.desktop_session = requests.Session()
        self.connect_desktop()

        self.mobile_session = requests.Session()
        self.connect_mobile()

    def connect_desktop(self):
        global parcoursup_url
        r = self.desktop_session.get(f"{parcoursup_url}authentification")
        r = self.try_onload(self.desktop_session, r)

        soup = BeautifulSoup(r.text, features="html.parser")

        form = soup.find('form', attrs={"name": "accesdossier"})
        if not form:
            return

        data = {input_.get("name"): input_.get("value")
                for input_ in form.findAll('input')}
        data["usermobile"] = False
        data["g_cn_cod"] = self.username
        data["g_cn_mot_pas"] = self.password

        parcoursup_url = r.url.replace('authentification', '')

        post_url = f"{parcoursup_url}{form.get('action')}"
        self.desktop_session.post(post_url, data=data)

    def get_html(self, to_file=False, path=None):
        dossier = self.desktop_session.get(f"{parcoursup_url}admissions")

        if not to_file:
            return dossier.text

        if not path:
            path = fr"{datetime.now().isoformat()}.html".replace(":", "-")

        with open(path, "w", encoding="utf-8") as f:
            f.write(dossier.text)
        return path

    def connect_mobile(self):
        data = {
            "appVersion": "2.2.1",
            "plateforme": "android",
            "plateformeVersion": "12",
            "session": datetime.now().year,
            "token": "".join(random.choices(list(string.ascii_letters + string.digits + string.punctuation), k=128))
        }

        token = self.mobile_session.post(f"{parcoursup_mobile}token",
                                         data=json.dumps(data), headers=JSON_HEADERS)
        if not token:
            raise Exception(f"{r.status_code} {r.reason}")

        data = {
            "code": self.password,
            "login": self.username,
            "tokenId": token.json()["tokenId"]
        }
        login = self.mobile_session.post(f"{parcoursup_mobile}login",
                                         data=json.dumps(data), headers=JSON_HEADERS)
        self.mobile_session.headers.update({"X-Auth-Token": login.headers.get("X-Auth-Token"),
                                            "Authorization": login.headers.get("Authorization"),
                                            "X-Token-Id": "356586",
                                            "X-Auth-Login": login.headers.get("X-Auth-Login")
                                            })
        if not login:
            raise Exception(f"{r.status_code} {r.reason}")

    def get_wishes(self):
        r = self.mobile_session.get(f"{parcoursup_mobile}voeux?liste=tous")
        if not r:
            raise Exception(f"{r.status_code} {r.reason}")
        return [Wish(w) for w in r.json()["voeux"]]

    def get_wish(self, id):
        r = self.mobile_session.get(f"{parcoursup_mobile}voeux/{id}")
        if not r:
            raise Exception(f"{r.status_code} {r.reason}")
        return Wish(r.json()["voeu"])

    @classmethod
    def try_onload(cls, s, r):
        soup = BeautifulSoup(r.text, features="html.parser")
        onload = soup.find('body').get("onload")
        if not onload:
            return r
        match = re.search(r"window.location='(?P<url>[^']*)'", onload)
        url = match.group('url')
        return cls.try_onload(s, s.get(url))

    @classmethod
    def is_open(cls) -> bool:
        r = requests.get(f"{parcoursup_url}authentification")
        r = cls.try_onload(requests, r)
        soup = BeautifulSoup(r.text, features="html.parser")
        return bool(soup.find('form', attrs={"name": "accesdossier"}))


class Wish:
    def __init__(self, json_dict):
        self.id = json_dict.get("voeuId")
        self.name = json_dict.get("formation")
        self.is_apprentissage = json_dict.get("formationEnApprentissage")
        self.etablissement = json_dict.get("etablissement")
        self.additional_infos = json_dict.get("infosComplementaires")

    def __new__(cls, json_dict):
        if cls != Wish:
            return super(Wish, cls).__new__(cls)

        state = json_dict["situation"]["code"]
        if state == 1:
            return Proposition(json_dict)
        elif state == 0:
            return PendingWish(json_dict)
        elif state == -1:
            return RefusedWish(json_dict)
        else:
            raise Exception("Unable to find state")

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __repr__(self):
        return f"<{type(self).__name__} {self.etablissement['nom']} {self.name}>"


class Proposition(Wish):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        self.reply_deadline = datetime.strptime(re.sub(r" \([^\)]*\)", "", json_dict["dateLimiteReponse"]), "%d %B %H:%M").replace(
            year=datetime.now().year, tzinfo=tz.gettz('Europe/Paris'))


class PendingWish(Wish):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        if json_dict.get("autresInformations"):
            soup = BeautifulSoup(json_dict["autresInformations"][0]["texte"], features="html.parser")
            strongs = [s for s in soup.findAll("strong") if s.text.isnumeric()]
            if len(strongs) == 6:
                self.waitlist_position = int(strongs[0].text)
                self.waitlist_lenght = int(strongs[1].text)
                self.nb_place = int(strongs[2].text)
                self.ranking_position = int(strongs[3].text)
                self.last_place = int(strongs[4].text)
                self.last_place_previous_year = int(strongs[5].text)
            elif len(strongs) == 2:
                self.ranking_position = int(strongs[0].text)
                self.nb_place = int(strongs[1].text)


class RefusedWish(Wish):
    def __init__(self, json_dict):
        super().__init__(json_dict)

        self.reason = json_dict["situation"]["libelle"]
