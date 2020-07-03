from CorpusDefinition import Corpus
import json
import csv
import os
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from preseeaspider.spiders.preseeabot import PreseeabotSpider


class PRESEEA(Corpus):
    """This class describes the PRESEEA Corpus and enables
       Webpage: https://preseea.linguas.net/Corpus.aspx

    Args:
        Corpus (class): General Corupus description
    """

    def __init__(self, search_phrase=""):
        """Generate a PRESEEA Corpus instance

        Args:
            search_phrase (str, optional): Phrase to search
                within corpus database. Defaults to "".
        """
        super().__init__('PRESEEA')

        # Open PRESEEA configuration file
        with open('preseea.json', 'r') as file:
            self._feature_dict = json.load(file)

        self.city_list = self.get_all_cities()
        self._search_phrase = search_phrase

    def set_search_phrase(self, phrase: str):
        """Set phrase to be searched within the Corus

        Args:
            phrase (str): Complete phrase with spaces e.g.
        """
        if type(phrase) is not str:
            raise ValueError('Phrase has to be of type string!')
        if any(umlaut in phrase for umlaut in ['ä', 'ö']):
            raise Warning('Spanish phrases should not contain umlauts')

        self._search_phrase = phrase

    def retrieve_phrase_data(self) -> list:
        """This method retrieves a list of phrases from an html document

        Returns:
            list: List of strings with phrases containing searched phrase
        """
        # Set up a crawler process to use a spider
        process = CrawlerProcess({
            'USER_AGENT': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                           (KHTML, like Gecko) Chrome/55.0.2883.75 \
                           Safari/537.36",
            'DOWNLOAD_TIMEOUT': 100,
            'REDIRECT_ENABLED': False,
            'SPIDER_MIDDLEWARES': {
                'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': True
            }
        })
        # Save crawled results iteratively within a list
        results = []

        # Signal process function definition
        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        # Middleware between downloader and spider
        dispatcher.connect(crawler_results, signal=signals.item_passed)

        # Apply requests from spider - Add arguments to initialize the spider
        process.crawl(PreseeabotSpider,
                      self._search_phrase,
                      self._city,
                      self._gender,
                      self._education,
                      self._age)
        _ = process.start()

        return results

    def write_csv(self, data: list, file_name: str):
        """Write current phrases' search results into csv

        Args:
            data (dict): retrieved data as dictionary
            file_name (str): csv file name
        """
        if len(data) == 0:
            return None

        for filter_key in ['text', 'date', 'country']:
            # Check first entry for necessary filters
            if filter_key not in list(data[0].keys()):
                raise KeyError('Unknown dictionary key: \
                                {} in crawled results!'.format(filter_key))

        if '.csv' not in file_name:
            file_name += '.csv'

        # Write into csv file
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write meta data
            keys_list = list(self._feature_dict.keys())
            writer.writerow(["Corpus", self._corpus_name])
            writer.writerow(["\n"])
            writer.writerow(["Filter:"])
            writer.writerow([keys_list[1], self._gender])
            writer.writerow([keys_list[2], self._age])
            writer.writerow([keys_list[3], self._education])
            writer.writerow([keys_list[4], self._city])
            writer.writerow(["Index", "Phrase"])
            writer.writerow(["\n"])

            # Write data
            for idx, phrase in enumerate(data):
                writer.writerow([idx,
                                 phrase['text'],
                                 phrase['date'],
                                 phrase['country']])

        return os.getcwd() + '/' + file_name
