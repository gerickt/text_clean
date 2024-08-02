from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text-clean",  # Reemplaza con el nombre de tu librería
    version="0.1.0",  # Inicia con una versión y actualízala con cada cambio
    author="Gerick Toro",
    author_email="gerickt@gmail.com",
    description="Librería para limpieza de texto en español.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gerickt/text-clean",  # URL de tu repositorio
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
    ],  # Agrega todas las dependencias necesarias
    python_requires=">=3.6",
)