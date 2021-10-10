from setuptools import setup

setup(
    name="bibliotheque",
    version="0.1",
    author="Cécile Le Mestre",
    description="Une bibliothèque",
    long_description=open("readme.txt").read(),
    packages=[
        "bibliotheque",
    ],  # folder name
    install_requires=[
        "numpy>=1.4",
    ],
)
