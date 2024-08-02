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

    def test_clean_text(self):
        corrections_dict = {'hola': ['holaa', 'holaaa']}
        text = 'holaa mundo! Visita https://example.com'
        expected = 'hola mundo visitar'
        self.assertEqual(clean_text(text, corrections_dict,
                         default_stopwords), expected)

    def test_process_text_column(self):
        data = pd.DataFrame(
            {'text': ['holaa mundo! Visita https://example.com']})
        corrections_dict = {'hola': ['holaa', 'holaaa']}
        result = process_text_column(
            data, 'text', corrections_dict, default_stopwords)
        self.assertEqual(result['Text_Clean'][0], 'hola mundo visitar')

    def test_load_stopwords(self):
        stopwords = load_stopwords('tests/test_stopwords.txt')
        self.assertIn('hola', stopwords)

    def test_load_corrections(self):
        corrections = load_corrections('tests/test_corrections.json')
        self.assertIn('hola', corrections)


if __name__ == '__main__':
    unittest.main()
