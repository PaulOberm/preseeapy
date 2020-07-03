import unittest
import mock
from CorpusPreseea import PRESEEA


class TestCorpusPreseeaClass(unittest.TestCase):
    def setUp(self):
        self.corpus_1 = PRESEEA()

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
        self.assertEqual(filter_list[1], 'Sex')
        self.assertEqual(filter_list[2], 'Age')
        self.assertEqual(filter_list[3], 'Education')
        self.assertEqual(filter_list[4], 'City')

    # Mock csv file!
    @mock.patch("builtins.open", create=True)
    def test_write_csv(self, csv_mock):
        test_data = [{'text': 'test_text',
                      'date': 'test_date',
                      'wrong_key': 'test_country'}]
        test_data_2 = [{'wrong_text_key': 'test_text',
                        'date': 'test_date',
                        'country': 'test_country'}]
        test_data_3 = [{'text': 'test_text',
                        'wrong_date': 'test_date',
                        'country': 'test_country'}]

        self.assertRaises(KeyError, self.corpus_1.write_csv,
                          **{'data': test_data, 'file_name': 'test'})
        self.assertRaises(KeyError, self.corpus_1.write_csv,
                          **{'data': test_data_2, 'file_name': 'test'})
        self.assertRaises(KeyError, self.corpus_1.write_csv,
                          **{'data': test_data_3, 'file_name': 'test'})

        test_data_correct = [{'text': 'test_text',
                              'date': 'test_date',
                              'country': 'test_country'}]
        file_name = 'test'
        csv_mock.side_effect = [
            mock.mock_open(read_data="foo").return_value]

        response = self.corpus_1.write_csv(data=test_data_correct,
                                           file_name=file_name)
        self.assertIn(file_name + '.csv', response)


if __name__ == '__main__':
    unittest.main()
