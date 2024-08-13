# text_clean/text_clean.py
import re
from unidecode import unidecode
from bs4 import BeautifulSoup
import html
import nltk
from nltk.corpus import stopwords
import json
import spacy
import emoji
from multiprocessing import Pool, cpu_count

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
    with open(file_path, 'r', encoding='utf-8') as file:
        corrections_dict = json.load(file)
    return corrections_dict


def apply_corrections(text, corrections_dict):
    if corrections_dict:
        for correct_value, variations in corrections_dict.items():
            for variation in variations:
                text = re.sub(r'\b{}\b'.format(
                    re.escape(variation.lower())), correct_value.lower(), text)
    return text


def extract_elements(text, pattern):
    return re.findall(pattern, text)


def clean_text(text, corrections_dict=None, stopwords_set=None, clean_type='all'):
    if not isinstance(text, str):
        return text

    urls, emojis, numbers = [], [], []

    if clean_type in ['all', 'url']:
        urls = extract_elements(
            text, r'\b((https?|ftp):\/\/[-\w]+(\.\w[-\w]*)+|www\.[-\w]+(\.\w[-\w]*)+|[-\w]+(\.\w[-\w]*)+)\S*')
        urls = [url[0] for url in urls]  # Extraer solo la URL completa
        text = remove_urls(text)

    if clean_type in ['all', 'html']:
        text = remove_html_tags(text)
        text = clean_html_entities(text)

    if clean_type in ['all', 'symbol']:
        text = remove_punctuation(text)

    if clean_type in ['all', 'number']:
        numbers = extract_elements(text, r'\d+')
        text = re.sub(r'\d+', '', text)  # Elimina números

    if clean_type in ['all', 'emoji']:
        emojis = [char for char in text if emoji.is_emoji(char)]
        text = ''.join([char for char in text if not emoji.is_emoji(char)])
        # Elimina signos de exclamación e interrogación
        text = re.sub(r'[!¡?¿]', '', text)

    text = re.sub(r'\s+', ' ', text).strip().lower()
    text = apply_corrections(text, corrections_dict)
    text = lemmatize_text(text)
    text = unidecode(text)

    if stopwords_set is not None:
        words = text.split()
        filtered_words = [word for word in words if word not in stopwords_set]
        clean_text = ' '.join(filtered_words)
    else:
        clean_text = text

    return clean_text, urls, emojis, numbers


def remove_html_tags(text):
    return BeautifulSoup(text, 'html.parser').get_text()


def clean_html_entities(text):
    if not isinstance(text, str):
        return text
    return html.unescape(text)


def remove_urls(text):
    if not isinstance(text, str):
        return text
    return re.sub(r'\b((https?|ftp):\/\/[-\w]+(\.\w[-\w]*)+|www\.[-\w]+(\.\w[-\w]*)+|[-\w]+(\.\w[-\w]*)+)\S*', '', text, flags=re.MULTILINE)


def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])


def process_text_column(data, column_name, corrections_dict=None, stopwords_set=None, clean_type='all'):
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_row, [(row, corrections_dict, stopwords_set, clean_type) for row in data[column_name]]
        )
    data['Text_Clean'], data['Text_URL'], data['Text_Emojis'], data['Text_Numbers'] = zip(*results)
    return data


def remove_punctuation(text):
    if not isinstance(text, str):
        return text
    return re.sub(r'[^\w\s]', '', text)

def process_row(row, corrections_dict, stopwords_set, clean_type):
    return clean_text(row, corrections_dict, stopwords_set, clean_type)

