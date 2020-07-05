import unittest
# import mock
from preseeapy.preseeaspider.spiders.preseeabot import PreseeabotSpider


class TestPreseeaBot(unittest.TestCase):
    def setUp(self):
        self._phrase = 'hago '
        self._city = 'Madrid'
        self._education = 'high'
        self._age = 'young'
        self._gender = 'female'
        self.spider = PreseeabotSpider(phrase=self._phrase,
                                       city=self._city,
                                       gender=self._gender,
                                       education=self._education,
                                       age=self._age)

    def test_map_to_city_key(self):
        """ Test the correct mapping of an city or location string
            to the used class name for crawling.
        """
        # Set expected return values
        correct_class_name_city = "dnn_ctr520_TranscriptionQuery_chkFtCity_11"

        # Run basic use cases and test
        retrieved_class_name_city = self.spider.map_to_city_key(self._city)
        self.assertEqual(correct_class_name_city,
                         retrieved_class_name_city)

        retrieved_class_name_city = self.spider.map_to_city_key('Pereira')
        self.assertNotEqual(correct_class_name_city,
                            retrieved_class_name_city)

        self.assertRaises(KeyError, self.spider.map_to_city_key,
                          **{'city': 'Minga'})

    def test_map_to_gender_key(self):
        """ Test the correct mapping of an gender string
            to the used class name for crawling.
        """
        # Set expected return values
        correct_class_name_female = "dnn_ctr520_TranscriptionQuery_chkFtSex_2"

        # Run basic use cases and test
        retrieved_class_name_female = self.spider.map_to_gender_key(self._gender)
        self.assertEqual(correct_class_name_female,
                         retrieved_class_name_female)

        retrieved_class_name_female = self.spider.map_to_gender_key('male')
        self.assertNotEqual(correct_class_name_female,
                            retrieved_class_name_female)

        # In honor to one of the greatest memes:
        # https://me.me/i/create-character-male-female-hardcore-create-cancel-finally-so-sick-7636818
        self.assertRaises(ValueError, self.spider.map_to_gender_key,
                          **{'gender': 'hardcore'})

    def test_map_to_age_key(self):
        """ Test the correct mapping of an age string
            to the used class name for crawling.
        """
        # Set expected return values
        correct_class_name_young = "dnn$ctr520$TranscriptionQuery$chkFtAgeGroup$1"

        # Run basic use cases and test
        retrieved_class_name_young = self.spider.map_to_age_key(self._age)
        self.assertEqual(correct_class_name_young, retrieved_class_name_young)

        retrieved_class_name_young = self.spider.map_to_age_key('old')
        self.assertNotEqual(correct_class_name_young,
                            retrieved_class_name_young)

        self.assertRaises(ValueError, self.spider.map_to_age_key,
                          **{'age': 'very_old'})

    def test_map_to_education_key(self):
        """ Test the correct mapping of an education string
            to the used class name for crawling.
        """
        # Set expected return values
        correct_class_name_education = "dnn$ctr520$TranscriptionQuery$chkFtStudyLevel$1"

        # Run basic use cases and test
        retrieved_class_name_education = self.spider.map_to_education_key(self._education)
        self.assertEqual(correct_class_name_education,
                         retrieved_class_name_education)

        retrieved_class_name_education = self.spider.map_to_education_key('low')
        self.assertNotEqual(correct_class_name_education,
                            retrieved_class_name_education)

        self.assertRaises(ValueError, self.spider.map_to_education_key,
                          **{'education': 'very_high'})
