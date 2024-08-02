import re
from unidecode import unidecode
from bs4 import BeautifulSoup
import html
import nltk
from nltk.corpus import stopwords
import json
import spacy
import string

# Descargar el modelo de spaCy
try:
    nlp = spacy.load("es_core_news_lg")
except OSError:
    spacy.cli.download("es_core_news_lg")
    nlp = spacy.load("es_core_news_lg")

# Descargar las stopwords en español, portugués e inglés
nltk.download('stopwords')
spanish_stopwords = set(stopwords.words('spanish'))
portuguese_stopwords = set(stopwords.words('portuguese'))
english_stopwords = set(stopwords.words('english'))

# Combinar stopwords de NLTK
default_stopwords = spanish_stopwords.union(
    portuguese_stopwords).union(english_stopwords)


def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        custom_stopwords = set(line.strip() for line in file)
    return custom_stopwords


def load_corrections(file_path):
    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        corrections_dict = json.load(file)
    return corrections_dict


def apply_corrections(text, corrections_dict):
    for correct_value, variations in corrections_dict.items():
        for variation in variations:
            text = re.sub(r'\b{}\b'.format(
                re.escape(variation.lower())), correct_value.lower(), text)
    return text


def clean_text(text, corrections_dict, stopwords_set):
    if not isinstance(text, str):
        return text
    text = remove_urls(text)
    text = remove_html_tags(text)
    text = clean_html_entities(text)
    text = remove_punctuation(text)  # Añadido aquí
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\d+', '', text)  # Elimina números
    text = text.lower()
    text = apply_corrections(text, corrections_dict)
    text = lemmatize_text(text)
    text = unidecode(text)

    words = text.split()
    filtered_words = [word for word in words if word not in stopwords_set]
    return ' '.join(filtered_words)


def remove_html_tags(text):
    return BeautifulSoup(text, 'html.parser').get_text()


def clean_html_entities(text):
    if not isinstance(text, str):
        return text
    return html.unescape(text)


def remove_urls(text):
    if not isinstance(text, str):
        return text
    return re.sub(r'(https?://|www\.)\S+', '', text, flags=re.MULTILINE)


def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])


def process_text_column(data, column_name, corrections_dict, stopwords_set):
    data['Text_Clean'] = data[column_name].apply(lambda x: clean_text(
        x, corrections_dict, stopwords_set) if isinstance(x, str) else x)
    return data

def remove_punctuation(text):
    if not isinstance(text, str):
        return text
    return text.translate(str.maketrans('', '', string.punctuation))
