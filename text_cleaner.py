import re
from unidecode import unidecode
from bs4 import BeautifulSoup
import html
import nltk
from nltk.corpus import stopwords
import json
import spacy

# Cargar el modelo de spaCy (descarga si es necesario)
try:
    nlp = spacy.load("es_core_news_lg")
except OSError:
    print("Descargando modelo de spaCy 'es_core_news_lg'...")
    spacy.cli.download("es_core_news_lg")
    nlp = spacy.load("es_core_news_lg")

# Descargar las stopwords en español, portugués e inglés (descarga si es necesario)
nltk.download('stopwords', quiet=True)
spanish_stopwords = set(stopwords.words('spanish'))
portuguese_stopwords = set(stopwords.words('portuguese'))
english_stopwords = set(stopwords.words('english'))

# Leer stopwords personalizadas desde un archivo (ajusta la ruta si es necesario)
with open('custom_stopwords.txt', 'r', encoding='utf-8') as file:
    custom_stopwords = set(line.strip() for line in file)

# Combinar stopwords de NLTK con las personalizadas
all_stopwords = spanish_stopwords.union(portuguese_stopwords).union(
    english_stopwords).union(custom_stopwords)

# Leer el diccionario de correcciones desde un archivo JSON (ajusta la ruta si es necesario)
with open('corrections.json', 'r', encoding='utf-8') as file:
    corrections_dict = json.load(file)


def apply_corrections(text, corrections_dict):
    """
    Función para aplicar correcciones en el texto usando un diccionario de variaciones.
    """
    for correct_value, variations in corrections_dict.items():
        for variation in variations:
            text = re.sub(r'\b{}\b'.format(
                re.escape(variation.lower())), correct_value.lower(), text)
    return text


def clean_text(text, corrections_dict):
    """
    Función principal para limpiar el texto.
    """
    if not isinstance(text, str):
        return text
    # Eliminar URLs
    text = remove_urls(text)
    # Eliminar etiquetas HTML
    text = remove_html_tags(text)
    # Convertir entidades HTML
    text = clean_html_entities(text)
    # Eliminar saltos de línea y símbolos
    text = re.sub(r'\s+', ' ', text)
    # Eliminar números
    text = re.sub(r'\d+', '', text)  # Elimina números
    # Convertir a minúsculas
    text = text.lower()
    # Aplicar correcciones
    text = apply_corrections(text, corrections_dict)
    # Lematizar ANTES de eliminar acentos
    text = lemmatize_text(text)
    # Remover acentos
    text = unidecode(text)

    # Eliminar stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in all_stopwords]
    return ' '.join(filtered_words)


def remove_html_tags(text):
    """
    Función para eliminar etiquetas HTML de una cadena de texto.
    """
    return BeautifulSoup(text, 'html.parser').get_text()


def clean_html_entities(text):
    """
    Función para convertir entidades HTML en sus caracteres correspondientes.
    """
    if not isinstance(text, str):
        return text
    return html.unescape(text)


def remove_urls(text):
    """
    Función para eliminar URLs de una cadena de texto. 
    """
    if not isinstance(text, str):
        return text
    return re.sub(r'(https?://|www\.)\S+', '', text, flags=re.MULTILINE)


def lemmatize_text(text):
    """
    Función para lematizar el texto usando spaCy.
    """
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])
