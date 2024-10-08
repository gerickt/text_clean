# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text_clean",
    version="0.1.3",
    author="Gerick Toro",
    author_email="gerickt@gmail.com",
    description="Librería para limpieza de texto en español.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gerickt/text_clean",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "beautifulsoup4",
        "unidecode",
        "nltk",
        "spacy",
        "pandas",
        "emoji",
    ],
    python_requires=">=3.6",
)
