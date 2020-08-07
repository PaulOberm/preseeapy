import unittest
from preseeapy.WordClassifier import WordClassifier


class TestWordClassifierClass(unittest.TestCase):
    def setUp(self):
        self.test_phrase = "?Hola, que tal?/ Finalmente has llegado aquí."
        self.classifier = WordClassifier(self.test_phrase)

    def test_get_word_list(self):
        returned_list = self.classifier.get_word_list(self.test_phrase)

        self.assertEqual(7, len(returned_list))
        self.assertEqual("tal?/", returned_list[2])

    def test_get_following_words(self):
        following_list = self.classifier.get_following_words("Finalmente")

        self.assertEqual(following_list[0], "has")
        self.assertEqual(following_list[2], "aquí.")

    def test_get_leading_words(self):
        leading_list = self.classifier.get_leading_words("Finalmente")

        self.assertEqual(leading_list[0], "?Hola,")

    def test_get_environment_words(self):
        leading_list, following_list = self.classifier.get_environment_words("Finalmente")

        self.assertEqual(leading_list[0], "?Hola,")
        self.assertEqual(following_list[0], "has")
