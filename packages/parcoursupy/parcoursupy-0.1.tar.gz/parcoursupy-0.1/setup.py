import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parcoursupy",
    version="0.1",
    description='Un python API wrapper pour Parcoursup',
    url="https://www.github.com/Bapt5/parcoursupy",
    author="Bapt5",
    license="MPL2.0",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.26.0",
        "beautifulsoup4>=4.10.0",
        "python-dateutil>=2.8.2"

    ]
)
