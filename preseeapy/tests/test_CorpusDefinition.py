import unittest
from CorpusDefinition import Corpus


class TestCorpusClass(unittest.TestCase):
    def setUp(self):
        self.corpus_1 = Corpus('PRESEEA')
    
    def test_get_corpus_name(self):
        self.assertEqual(self.corpus_1.get_corpus_name(), 'PRESEEA')