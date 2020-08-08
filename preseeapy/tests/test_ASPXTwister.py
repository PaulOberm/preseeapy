import unittest
from preseeapy.ASPXTwister import ASPXTwister


class TestASPXTwisterClass(unittest.TestCase):
    def setUp(self):
        self.test_phrase = "?Hola, que tal?/ Finalmente has llegado aquí."
        self.classifier = WordClassifier(self.test_phrase)

    def test_get_word_list(self):
        returned_list = self.classifier.get_word_list(self.test_phrase)

        self.assertEqual(7, len(returned_list))
        self.assertEqual("tal?/", returned_list[2])