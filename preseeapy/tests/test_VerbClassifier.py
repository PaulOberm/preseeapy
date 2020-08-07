import unittest
from preseeapy.VerbClassifier import VerbClassifier


class TestVerbClassifierClass(unittest.TestCase):
    def setUp(self):
        self.test_list = ["Hola", "llamo", "vamos",
                          "abren", "ves", "echan", "voy", "no!"]
        self.classifier = VerbClassifier(self.test_list)

    def test_set_word_list(self):
        manipulated_list = self.test_list + [0]
        self.classifier.set_word_list(manipulated_list)

        # Assert that 0 is not part of the instances word list
        returned_list = self.classifier.get_word_list()
        self.assertNotEqual(len(returned_list), len(manipulated_list))
        self.assertEqual(len(self.test_list), len(returned_list))
        self.assertEqual(returned_list[-1], "no")

    def test_classify_verbs(self):
        classified_verbs = self.classifier.classify_verbs()

        # Assert tested method
        self.assertEqual(classified_verbs['1ps_sg'][0], self.test_list[1])
        self.assertEqual(classified_verbs['1ps_pl'][0], self.test_list[2])

    def test_is_3person_plural(self):
        test_word = 'me'
        is_3p_pl_verb = self.classifier.is_3person_plural(test_word)
        self.assertFalse(is_3p_pl_verb)

        test_word = 'eran'
        is_3p_pl_verb = self.classifier.is_3person_plural(test_word)
        self.assertTrue(is_3p_pl_verb)

    def test_is_2person_plural(self):
        test_word = 'me'
        is_2p_pl_verb = self.classifier.is_2person_plural(test_word)
        self.assertFalse(is_2p_pl_verb)

        test_word = 'sois'
        is_2p_pl_verb = self.classifier.is_2person_plural(test_word)
        self.assertTrue(is_2p_pl_verb)
