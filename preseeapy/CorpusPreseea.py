from .CorpusDefinition import Corpus
from twisted.internet import reactor
import json
import csv
import itertools as it
import os
from multiprocessing import Process, Queue
from scrapy.signalmanager import dispatcher
import types
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy import signals
from .preseeaspider.spiders.preseeabot import PreseeabotSpider


class ProcessHandler():
    def __init__(self, attach_function: types.FunctionType):
        if not hasattr(attach_function, '__call__'):
            raise ValueError("Attach function object to ProcessHandler!")

        self._queue = Queue()
        self._process = self._start_process(attach_function)

    def _start_process(self, function) -> Process:
        """Start a parallel thread to run the twisted reactor in.

        Args:
            queue (multiprocessing.Queue): [description]

        Returns:
            multiprocessing.Process: [description]
        """
        p = Process(target=function,
                    args=(self._queue,))
        p.start()

        return p

    def get_queue_content(self):
        content = self._queue.get()

        return content

    def close(self):
        self._process.join()


class PRESEEA(Corpus):
    """This class describes the PRESEEA Corpus and enables
       scraping webpage: https://preseea.linguas.net/Corpus.aspx

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
        with open('preseeapy/preseea.json', 'r') as file:
            self._feature_dict = json.load(file)

        self._city = ""
        self._gender = ""
        self._age = ""
        self._education = ""

        self.SET_PROCESS = False

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
        """Retrieve phrase data with a separate process' thread

        Returns:
            list: List of dictionaries with phrases and PRESEEA metadata
        """
        process_instance = ProcessHandler(self._retrieve_phrase_data_subprocess)

        phrase_list = process_instance.get_queue_content()
        process_instance.close()

        return phrase_list

    def _retrieve_phrase_data_subprocess(self, queue: Queue) -> list:
        """This method retrieves a list of phrases from an html document

        Returns:
            list: List of strings with phrases containing searched phrase
        """
        # Set up a crawler process to use a spider
        # process = CrawlerProcess({
        runner = CrawlerRunner({
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
        dispatcher.connect(reactor.stop, signal=signals.spider_closed)

        # Apply requests from spider - Add arguments to initialize the spider
        if self._check_filter_parameters():
            try:
                defered = runner.crawl(PreseeabotSpider,
                            self._search_phrase,
                            self._city,
                            self._gender,
                            self._education,
                            self._age)

                defered.addBoth(lambda _: reactor.stop())

                reactor.run()
                queue.put(results)
            except Exception as e:
                queue.put(e)
        else:
            queue.put(None)

    def _check_filter_parameters(self) -> bool:
        """Check the given filter parameters for a POST request.

        Returns:
            bool: Return true if POST request is possible
        """
        check_filters = True

        # Check all filters for availability
        if self._city == "":
            check_filters = False
        if self._gender == "":
            check_filters = False
        if self._education == "":
            check_filters = False
        if self._age == "":
            check_filters = False
        if self._search_phrase == "":
            check_filters = False

        print('Parameters checked: {}'.format(str(check_filters)))

        return check_filters

    def write_csv(self, data: list, file_name: str):
        """Write current phrases' search results into csv

        Args:
            data (dict): retrieved data as dictionary
            file_name (str): csv file name
        """
        if data is None:
            return None
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
            writer.writerow(["Phrase", self._search_phrase])
            writer.writerow(["\n"])
            writer.writerow(["Found number of entries", len(data)])
            writer.writerow(["Index", "Text"])
            writer.writerow(["\n"])
            writer.writerow(["\n"])

            # Write data
            for idx, phrase in enumerate(data):
                # Write data 1-indexed
                writer.writerow([idx+1,
                                 phrase['label'],
                                 phrase['text'],
                                 phrase['date'],
                                 phrase['country']])

        return os.getcwd() + '/' + file_name

    def analyse(self, data: list):
        """Analse the given data according to basic statistical measures

        Args:
            data (list): Retrieved data from preseea
        """

        return 0

    def set_city(self, name: str):
        """Set Corpus' instance city by its name and check beforehand

        Args:
            name (str): Name of the city the corpus should be filtered on
        """
        # city_list = self.get_all_cities()
        city_list = list(self._feature_dict['City'].keys())
        if name in city_list:
            self._city = name
        elif name == "all":
            self._city = "all"
        else:
            Warning('Given location or city: \
                {} is not defined'.format(name))
            self._city = ""

    def set_sex(self, name: str):
        """Set Corpus' instance gender by its name and check beforehand

        Args:
            name (str): Name of the gender the corpus should be filtered on
        """
        sex_list = self._feature_dict['Sex']
        if name in sex_list:
            self._gender = name
        elif name == "all":
            self._gender = "all"
        else:
            Warning('Gender not in accordance with corpus')
            self._gender = ""

    def set_age(self, name: str):
        """Set Corpus' instance age by its name and check beforehand

        Args:
            name (str): Name of the age the corpus should be filtered on
        """
        age_list = self._feature_dict['Age']
        if name in age_list:
            self._age = name
        elif name == "all":
            self._age = "all"
        else:
            Warning('Age definition not in accordance with corpus')
            self._age = ""

    def set_education(self, name: str):
        """Set Corpus' instance education by its name and check beforehand

        Args:
            name (str): Name of the education the corpus should be filtered on
        """
        education_list = self._feature_dict['Education']
        if name in education_list:
            self._education = name
        elif name == "all":
            self._education = "all"
        else:
            Warning('Education definition not in accordance with corpus')
            self._education = ""

    def set_filter(self, city: str, gender: str,
                   age: str, education: str, phrase: str):
        self.set_city(city)
        self.set_sex(gender)
        self.set_age(age)
        self.set_education(education)
        self.set_search_phrase(phrase)

        filter_name = "preseea_{}_{}_{}_{}_{}".format(city, gender, age, education, phrase)

        return filter_name

    def get_filter(self):
        city = 'City: {}'.format(self._city)
        gender = 'Gender: {}'.format(self._gender)
        age = 'Age: {}'.format(self._age)
        education = 'Education: {}'.format(self._education)

        return '{}, {}, {}, {}'.format(city, gender, age, education)

    def get_corpus_countries(self):
        """Return the Corpus' establishing countries.

        Returns:
            list: List of strings of the countries
        """
        countries = self._feature_dict["Country"].keys()

        return countries

    def get_all_cities(self) -> list:
        """Return all the available cities in the Corpus

        Returns:
            list: List of strings with the city names
        """

        temporary_city_list = []
        for country in self.get_corpus_countries():
            temporary_city_list.append(self._feature_dict["Country"][country])

        city_list = list(it.chain.from_iterable(temporary_city_list))

        return city_list

    def _check_city(self, sample: str) -> list:
        """Check if samples are available for that feature

        Args:
            sample (str): Sample name, e.g. Colombia

        Returns:
            list: List of strings with available samples
        """

        # Compare demanded sample with the available feature list
        try:
            feature_list = self._feature_dict["Country"][sample]
        except KeyError:
            raise KeyError('{} not available in Corpus'.format(sample))

        return feature_list

    def get_cities(self, country: str) -> list:
        """Return the cities available in the given country

        Args:
            country (str): Country within the Corpus

        Returns:
            list: List of strings with the available cities
        """
        city_list = self._check_city(country)

        return city_list

    def get_number_cities(self, country: str) -> int:
        """Return the number of available cities per country

        Args:
            country ([type]): Name of the country
        Returns:
            int: Number of cities to be returned for country
        """
        city_list = self.get_cities(country)
        number_cities = len(city_list)

        return number_cities

    def get_number_all_cities(self) -> int:
        """Return the number of all available Corpus cities

        Returns:
            int: Number of available cities
        """

        city_list = self.get_all_cities()
        number_cities = len(city_list)

        return number_cities