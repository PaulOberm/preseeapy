import unittest
import mock
from preseeapy.utils import ProcessHandler
from preseeapy.PRESEEA import PRESEEA


class TestCorpusPreseeaClass(unittest.TestCase):
    def setUp(self):
        self._city = "Pereira"
        self._gender = "Mujer"
        self._age = "Grupo 1"
        self._education = "Alto"
        self._phrase = "se "
        self.corpus_1 = PRESEEA("test", " ")

        self.data = [{"text": "test",
                      "label": "test",
                      "date": "test",
                      "country": "test"}]

    def test_get_corpus_name(self):
        self.assertEqual(self.corpus_1.get_corpus_name(), 'PRESEEA')

    def test_set_search_phrase(self):
        self.assertRaises(Warning, self.corpus_1.set_search_phrase, 'täst')
        self.assertRaises(ValueError, self.corpus_1.set_search_phrase, 5)

    def test_get_cities(self):
        self.assertIn('Madrid', self.corpus_1.get_cities('Spain'),
                      'Incorrect corpus. A spanish \
                       corpus should contain Madrid')
        self.assertIn('Bogotá', self.corpus_1.get_cities('Colombia'),
                      'Incorrect corpus. A spanish \
                       corpus should containi Bogotá')

        self.assertRaises(KeyError, self.corpus_1.get_cities,
                          **{'country': 'Testcountry'})

    def test_get_number_cities(self):
        self.assertGreaterEqual(self.corpus_1.get_number_cities('Spain'), 1)

    def test_corpus_definition(self):
        filter_list = list(self.corpus_1._feature_dict.keys())
        self.assertEqual(filter_list[1], 'Gender')
        self.assertEqual(filter_list[2], 'Age')
        self.assertEqual(filter_list[3], 'Education')
        self.assertEqual(filter_list[4], 'City')

    # Mock csv file!
    @mock.patch("builtins.open", create=True)
    def test_write_csv(self, csv_mock):
        test_data = [{'text': 'test_text',
                      'date': 'test_date',
                      'label': 'test_label',
                      'wrong_key': 'test_country'}]
        test_data_2 = [{'wrong_text_key': 'test_text',
                        'date': 'test_date',
                        'label': 'test_label',
                        'country': 'test_country'}]
        test_data_3 = [{'text': 'test_text',
                        'wrong_date': 'test_date',
                        'label': 'test_label',
                        'country': 'test_country'}]

        self.assertRaises(KeyError, self.corpus_1.write_csv,
                          **{'data': test_data, 'meta': 1, 'file_name': 'test'})
        self.assertRaises(KeyError, self.corpus_1.write_csv,
                          **{'data': test_data_2, 'meta': 1, 'file_name': 'test'})
        self.assertRaises(KeyError, self.corpus_1.write_csv,
                          **{'data': test_data_3, 'meta': 1, 'file_name': 'test'})

        test_data_correct = [{'text': 'test_text',
                              'date': 'test_date',
                              'label': 'test_label',
                              'country': 'test_country'}]
        file_name = 'test'
        csv_mock.side_effect = [
            mock.mock_open(read_data="foo").return_value]

        response = self.corpus_1.write_csv(data=test_data_correct,
                                           meta={'Total samples': 1,
                                                 'Name': 'Test'},
                                           file_name=file_name)
        self.assertIn(file_name + '.csv', response)

    # def test_get_verbs(self):
    #     test_word_list = [['con', 'me'], ['eran', 'listo'], ['estais', 'locos']]
    #     verb_list = self.corpus_1.get_verbs(test_word_list)

    #     self.assertEqual(len(verb_list), len(test_word_list))
    #     self.assertEqual(verb_list[1]['2ps_pl'], 'eran')
    #     self.assertEqual(verb_list[2]['3ps_pl'], 'estais')

    # @mock.patch("ProcessHandler.get_queue_content", [{"test: test"}])
    def test_ProcessHandler(self):
        self.assertRaises(ValueError, ProcessHandler, 5)

    def test_set_filter(self):
        self.corpus_1.set_filter(city=self._city,
                                 gender=self._gender,
                                 age=self._age,
                                 education=self._education,
                                 phrase=self._phrase)
        filter_name = str(self.corpus_1)
        # Test if responded filter name contains filter attributes
        self.assertIn(self._city, filter_name)
        self.assertIn(self._gender, filter_name)
        self.assertIn(self._age, filter_name)
        self.assertIn(self._education, filter_name)
        self.assertIn(self._phrase, filter_name)

    def test_get_leading_words(self):
        test_phrase = "…  desde / desde que"
        number_words = 2
        test_words = self.corpus_1.get_leading_words(test_phrase, number_words)
        self.assertEqual(len(test_words), number_words)
        test_words = self.corpus_1.get_leading_words(test_phrase, 100)
        self.assertEqual(len(test_words), 3)

    def test_get_following_words(self):
        test_phrase = "erais pequeños / y todo eso / siempre …"
        number_words = 2

        test_words = self.corpus_1.get_following_words(test_phrase, number_words)
        self.assertEqual(len(test_words), number_words)

        test_words = self.corpus_1.get_following_words(test_phrase, 100)
        self.assertEqual(len(test_words), 6)

    def test_get_environment_words(self):
        test_phrase = "…  desde / desde que   ustedes  erais\
              pequeños / y todo eso / siempre …"
        self.corpus_1.set_search_phrase("ustedes")

        leading_list, following_list = self.corpus_1.get_environment_words({'text': test_phrase})

        self.assertEqual(len(leading_list), 3)
        self.assertEqual(len(following_list), 3)

    @mock.patch("preseeapy.PRESEEA.retrieve_city_info",
                return_value=10)
    def test_analyse(self, mocked_method):
        self.corpus_1.set_search_phrase("ustedes")
        test_phrase = "…  desde / desde que   ustedes  erais\
              pequeños / y todo eso / siempre …"
        test_list = [{'text': test_phrase}]

        analysed_data = self.corpus_1.analyse(samples_list=test_list)
        self.assertEqual(len(analysed_data['Leading']), len(test_list))
        self.assertEqual(len(analysed_data['Following']), len(test_list))

        self.assertEqual(analysed_data['Leading'][0][0], "desde")
        self.assertEqual(analysed_data['Leading'][0][1], "desde")
        self.assertEqual(analysed_data['Following'][0][0], "erais")
        self.assertEqual(analysed_data['Following'][0][1], "pequeños")
        self.assertNotEqual(analysed_data['Following'][0][1], "pequeños test")

        self.assertEqual(analysed_data['Total samples'],
                         mocked_method.return_value)

    @mock.patch("preseeapy.utils.ProcessHandler.get_queue_content",
                return_value=[{"test": "test"}])
    def test_retrieve_phrase_data(self, queue_content_patch):
        """Test the retrievement of phrases for a specific filter
           on PRESEEA

        Args:
            queue_content_patch (dictionary): The final retrievement
                runs with a subprocess function and returns a list
                of dictionaries. Each of which refers to a phrase.
        """
        results = self.corpus_1.retrieve_phrase_data()

        # Test if responded result is empty, since no city is defined
        self.assertEqual([{"test": "test"}], results)

    @mock.patch("preseeapy.PRESEEA.retrieve_phrase_data",
                return_value=[{"test": "test"}, {"test": "test"}])
    def test_get_number_city_samples(self, retrieved_sample_list):
        n_samples = 2
        search_phrase = "Hola"
        self.corpus_1.set_search_phrase(search_phrase)

        # Function under test
        n_sample_test = self.corpus_1.get_number_samples()

        # Assert correct response
        self.assertEqual(n_samples, n_sample_test)

        # Assert unchanged search phrase
        self.assertEqual(self.corpus_1.get_search_phrase(), search_phrase)

    @mock.patch("preseeapy.PRESEEA.retrieve_phrase_data",
                return_value=[{"test": "test"}, {"test": "test"}])
    def test_retrieve_city_info(self, mocked_list):
        self.corpus_1.set_city('Madrid')
        n_samples = self.corpus_1.retrieve_city_info()
        self.assertEqual(len(mocked_list.return_value), n_samples)

        self.corpus_1.set_city('Unavailable')
        n_test = self.corpus_1.retrieve_city_info()
        self.assertIsNone(n_test)

    @mock.patch("preseeapy.PRESEEA.retrieve_phrase_data",
                return_value=[{'label': 'MADR_H13_013', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-02-27', 'country': 'España'}, {'label': 'MADR_H23_033', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-02-27', 'country': 'España'}, {'label': 'MADR_H33_049', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2007-09-06', 'country': 'España'}, {'label': 'MADR_M13_018', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-04-20', 'country': 'España'}, {'label': 'MADR_M23_034', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-06-24', 'country': 'España'}, {'label': 'MADR_M33_054', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-09-23', 'country': 'España'}, {'label': ' MADR_H12_007', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2012-07-11', 'country': 'España'}, {'label': ' MADR_H22_026', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2011-03-16', 'country': 'España'}, {'label': ' MADR_H32_043', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2011-05-03', 'country': 'España'}, {'label': ' MADR_M12_010', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2013-12-12', 'country': 'España'}, {'label': ' MADR_M22_030', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2009-11-10', 'country': 'España'}, {'label': ' MADR_M32_047', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2011-08-10', 'country': 'España'}, {'label': ' MADR_H11_002', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-12-04', 'country': 'España'}, {'label': ' MADR_H21_020', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2009-02-23', 'country': 'España'}, {'label': ' MADR_H31_037', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2009-01-29', 'country': 'España'}, {'label': ' MADR_ M11_004', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-11-25', 'country': 'España'}, {'label': ' MADR_M21_024', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2008-12-15', 'country': 'España'}, {'label': ' MADR_M31_040', 'text': '">[ Sin coincidencias de texto ]</span>', 'date': '2009-02-17', 'country': 'España'}])
    def test_analyse_madrid(self, samples_list_madrid):
        pass


if __name__ == '__main__':
    unittest.main()
