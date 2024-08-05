import unittest
from text_clean.text_clean import (
    load_stopwords,
    load_corrections,
    apply_corrections,
    clean_text,
    remove_html_tags,
    clean_html_entities,
    remove_urls,
    lemmatize_text,
    process_text_column,
    remove_punctuation,
    default_stopwords
)
import pandas as pd


class TestTextClean(unittest.TestCase):

    def test_remove_html_tags(self):
        self.assertEqual(remove_html_tags('<p>Hola</p>'), 'Hola')

    def test_clean_html_entities(self):
        self.assertEqual(clean_html_entities(
            'Hola &amp; adiós'), 'Hola & adiós')

    def test_remove_urls(self):
        self.assertEqual(remove_urls('Visita https://example.com'), 'Visita ')

    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation('Hola, mundo!'), 'Hola mundo')

    def test_apply_corrections(self):
        corrections_dict = {'hola': ['holaa', 'holaaa']}
        self.assertEqual(apply_corrections(
            'holaa mundo', corrections_dict), 'hola mundo')

    def test_clean_text_all(self):
        corrections_dict = {'hola': ['holaa', 'holaaa']}
        text = 'holaa mundo! Visita https://example.com'
        expected_clean = 'hola mundo visitar'
        clean, urls, emojis, numbers = clean_text(
            text, corrections_dict, default_stopwords, 'all')
        self.assertEqual(clean, expected_clean)
        self.assertEqual(urls, ['https://example.com'])
        self.assertEqual(emojis, [])
        self.assertEqual(numbers, [])

    def test_clean_text_url(self):
        text = 'Visita https://example.com para más información'
        expected_clean = 'visita informacion'
        clean, urls, emojis, numbers = clean_text(
            text, None, default_stopwords, 'url')
        self.assertEqual(clean, expected_clean)
        self.assertEqual(urls, ['https://example.com'])

    def test_clean_text_number(self):
        text = 'Tengo 2 manzanas y 3 peras'
        expected_clean = 'tener manzana pera'
        clean, urls, emojis, numbers = clean_text(
            text, None, default_stopwords, 'number')
        self.assertEqual(clean, expected_clean)
        self.assertEqual(numbers, ['2', '3'])

    def test_clean_text_emoji(self):
        text = '¡Hola! 😊 ¿Cómo estás?'
        expected_clean = 'hola'
        clean, urls, emojis, numbers = clean_text(
            text, None, default_stopwords, 'emoji')
        self.assertEqual(clean, expected_clean)
        self.assertEqual(emojis, ['😊'])

    def test_process_text_column(self):
        data = pd.DataFrame(
            {'text': ['holaa mundo! Visita https://example.com']})
        corrections_dict = {'hola': ['holaa', 'holaaa']}
        result = process_text_column(
            data, 'text', corrections_dict, default_stopwords, 'all')
        self.assertEqual(result['Text_Clean'][0], 'hola mundo visitar')
        self.assertEqual(result['Text_URL'][0], ['https://example.com'])
        self.assertEqual(result['Text_Emojis'][0], [])
        self.assertEqual(result['Text_Numbers'][0], [])

    def test_load_stopwords(self):
        stopwords = load_stopwords('tests/test_stopwords.txt')
        self.assertIn('hola', stopwords)

    def test_load_corrections(self):
        corrections = load_corrections('tests/test_corrections.json')
        self.assertIn('hola', corrections)


if __name__ == '__main__':
    unittest.main()
