from CorpusDefinition import Corpus
import json
import csv
import itertools as it
from bs4 import BeautifulSoup


class PRESEEA(Corpus):
    """This class describes the PRESEEA Corpus and enables
       Webpage: https://preseea.linguas.net/Corpus.aspx

    Args:
        Corpus (class): General Corupus description
    """

    def __init__(self):
        """Generate a PRESEEA Corpus instance
        """
        super().__init__('PRESEEA')
        with open('preseea.json', 'r') as file:
            self._feature_list = json.load(file)

        self.city_list = self.get_all_cities()
        self._search_phrase = ""

    def set_search_phrase(self, phrase: str):
        """Set phrase to be searched within the Corus

        Args:
            phrase (str): Complete phrase with spaces e.g.
        """

        self._search_phrase = phrase

    def retrieve_phrase_data(self) -> list:
        """This method retrieves a list of phrases from an html document

        Returns:
            list: List of strings with phrases containing searched phrase
        """
        # with open("example2.html") as file: 
        #     test = file.read()
        # test_result = BeautifulSoup(test, 'html.parser')

        # result = self.get_results()
        # span_list = result.find_all('span')

        # # Get text matches
        # data_list = result.find_all('span', id=lambda x: x and x.endswith('TextMatch'))
        # text_list = [data.text for data in data_list]

        text_list = ['dummy']

        return text_list

    def write_csv(self, file_name: str):
        """Write current phrases' search results into csv

        Args:
            file_name (str): csv file name
        """
        # # Get data to write
        # phrases_list = self.retrieve_phrase_data("example2.html")

        # # Write into csv file
        # with open(file_name, 'w', newline='') as file:
        #     writer = csv.writer(file)

        #     # Write meta data
        #     writer.writerow(["Corpus", self._corpus_name])
        #     wrtier.writerow(["\n"])
        #     writer.writerow(["Filter"])
        #     writer.writerow(["City", self._city])
        #     writer.writerow(["Sex", self._gender])
        #     writer.writerow(["Age", self._age])
        #     writer.writerow(["Education", self._education])
        #     writer.writerow(["Index", "Phrase"])
        #     wrtier.writerow(["\n"])

        #     # Write data
        #     for idx, phrase in enumerate(phrases_list):
        #         writer.writerow([idx, phrase])

        pass
