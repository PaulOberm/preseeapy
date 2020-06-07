import unittest
from CorpusPreseea import PRESEEA


class TestCorpusPreseeaClass(unittest.TestCase):
    def setUp(self):
        self.corpus_1 = PRESEEA()
    
    def test_get_corpus_name(self):
        self.assertEqual(self.corpus_1.get_corpus_name(), 'PRESEEA')
    
    def test_get_cities(self):
        self.assertIn('Madrid', self.corpus_1.get_cities('Spain'), 
                      'Incorrect corpus. A spanish corpus should contain Madrid')
        self.assertIn('Bogotá', self.corpus_1.get_cities('Colombia'),
                      'Incorrect corpus. A spanish corpus should containi Bogotá')

        self.assertRaises(KeyError, self.corpus_1.get_cities, **{'country': 'Testcountry'})
        # self.assertRaises(KeyError, self.corpus_1.get_cities('Testcountry'))
    
    def test_get_number_cities(self):
        self.assertGreaterEqual(self.corpus_1.get_number_cities('Spain'), 1)