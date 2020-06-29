from CorpusDefinition import Corpus
import json
import csv
import itertools as it
from bs4 import BeautifulSoup
import scrapy
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
            self._feature_list = json.load(file)

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
        process = CrawlerProcess({
            'USER_AGENT': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
            'DOWNLOAD_TIMEOUT':100,
            'REDIRECT_ENABLED':False,
            'SPIDER_MIDDLEWARES' : {
                'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware':True
            }
        })

        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_passed)

        process.crawl(PreseeabotSpider)
        test = process.start()

        return results

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
