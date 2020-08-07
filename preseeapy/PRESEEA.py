from .CorpusDefinition import Corpus
from twisted.internet import reactor
import json
import csv
import os
from multiprocessing import Queue
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from .preseeaspider.spiders.preseeabot import PreseeabotSpider
from .utils import ProcessHandler
from .CityCorpusMixin import CityCorpusMixin
from .AgeCorpusMixin import AgeCorpusMixin
from .GenderCorpusMixin import GenderCorpusMixin
from .EducationCorpusMixin import EducationCorpusMixin
from .VerbClassifier import VerbClassifier
from .WordClassifier import WordClassifier


class PRESEEA(Corpus, CityCorpusMixin, AgeCorpusMixin,
              GenderCorpusMixin, EducationCorpusMixin):
    """This class describes the PRESEEA corpus and enables
       scraping its webpage: https://preseea.linguas.net/Corpus.aspx

    Args:
        Corpus (class): General Corpus description
    """

    def __init__(self, author: str, search_phrase=""):
        """Generate a PRESEEA corpus instance.

        Args:
            search_phrase (str, optional): Phrase to search
                within corpus database. Defaults to "".
        """
        super().__init__('PRESEEA', author, search_phrase)

        # Open PRESEEA configuration file to load available features
        with open('preseeapy/preseea.json', 'r') as file:
            self._feature_dict = json.load(file)

        # PRESEEA specifc filter values
        self.set_city("")
        self.set_gender("")
        self.set_age("")
        self.set_education("")

    def __str__(self):
        return "PRESEEA" + "_"\
            + CityCorpusMixin.__str__(self) + "_"\
            + GenderCorpusMixin.__str__(self) + "_"\
            + AgeCorpusMixin.__str__(self) + "_"\
            + EducationCorpusMixin.__str__(self) + "_"\
            + "Phrase_" + self.get_search_phrase()

    def retrieve_phrase_data(self) -> list:
        """Retrieve phrase data with a separate process.

        Returns:
            list: List of dictionaries with phrases
                and PRESEEA metadata
                meta: date, sample number, country
        """
        # Initialize a subprocess instance
        attach_function = self._retrieve_phrase_data_subprocess
        process_instance = ProcessHandler(attach_function)

        # Execute attached function on subprocess
        phrase_list = process_instance.get_queue_content()
        process_instance.close()

        return phrase_list

    def get_number_samples(self) -> int:
        """Get number of samples for a specific phrase.

        Returns:
            [int]: Number of samples for given phrase
                and filter
        """
        total_list = self.retrieve_phrase_data()
        n_total = len(total_list)

        return n_total

    def _retrieve_phrase_data_subprocess(self, queue: Queue) -> list:
        """This method retrieves a list of phrases from an html document

        Returns:
            list: List of strings with phrases containing searched phrase
        """
        # Set up a crawler process to use a spider
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
            bool: Return true if filter features are set, so that
                POST request is possible
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

        return check_filters

    def _write_section(self, writer: csv.writer, titel: str, content: str):
        writer.writerow([titel, content])
        writer.writerow(["\n"])

        return writer

    def _write_meta_data(self, writer: csv.writer, meta: dict):
        writer = self._write_section(writer, "Corpus", self._corpus_name)
        writer = self._write_section(writer, "User", meta['Name'])
        writer.writerow(["Code", "", "https://github.com/PaulOberm/preseeapy"])
        writer.writerow(["Download", "", "https://test.pypi.org/project/preseeapy/"])

        keys_list = list(self._feature_dict.keys())
        writer.writerow(["Filter:"])
        writer.writerow([keys_list[1], self._gender])
        writer.writerow([keys_list[2], self._age])
        writer.writerow([keys_list[3], self._education])
        writer.writerow([keys_list[4], self._city])

        writer = self._write_section(writer, "Phrase", self._search_phrase)
        writer = self._write_section(writer,
                                     "Samples total",
                                     meta['Total samples'])

        # Get following verbs for 3PS_PL
        if "Leading verbs" in meta:
            verbs_anterior_2ps_pl = []
            verbs_anterior_3ps_pl = []
            for phrase in meta["Leading verbs"]:
                if phrase["2ps_pl"] is not None:
                    verbs_anterior_2ps_pl.append(phrase["2ps_pl"])
                elif phrase["3ps_pl"] is not None:
                    verbs_anterior_3ps_pl.append(phrase["3ps_pl"])

            writer.writerow(["Leading verbs"])
            writer.writerow(["#2PS, PL", len(verbs_anterior_2ps_pl)])
            writer.writerow(["#3PS, PL", len(verbs_anterior_3ps_pl)])
            len_total_1 = len(verbs_anterior_2ps_pl) + len(verbs_anterior_3ps_pl)


        if "Following verbs" in meta:
            verbs_posterior_2ps_pl = []
            verbs_posterior_3ps_pl = []
            for phrase in meta["Following verbs"]:
                if phrase["2ps_pl"] is not None:
                    verbs_posterior_2ps_pl.append(phrase["2ps_pl"])
                elif phrase["3ps_pl"] is not None:
                    verbs_posterior_3ps_pl.append(phrase["3ps_pl"])

            writer.writerow(["Following verbs"])
            writer.writerow(["#2PS, PL", len(verbs_posterior_2ps_pl)])
            writer.writerow(["#3PS, PL", len(verbs_posterior_3ps_pl)])
            len_total_2 = len(verbs_posterior_2ps_pl) + len(verbs_posterior_3ps_pl)
            writer.writerow(["#Verbs total", len_total_1+len_total_2])

        return writer

    def get_verbs(self, word_list: list) -> list:
        """Get a list of verbs from a list of words

        Args:
            word_list (list): A list of of lists of words

        Returns:
            list: A sublist with verbs
        """
        verb_list = []
        classifier = VerbClassifier([""])
        for sample_words in word_list:
            classifier.set_word_list(sample_words)
            classified_word = classifier.classify_verbs()
            verb_list.append(classified_word)

        return verb_list

    def write_csv(self, data: list, meta: dict):
        """Write current phrases' search results into csv

        Args:
            data (dict): retrieved data as dictionary
            meta_data (dict): General information referring corpus data
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

        # Write into csv file
        file_name = "report/{}.csv".format(self.__str__())
        if not os.path.exists(file_name.split('/')[0]):
            os.makedirs(file_name.split('/')[0])
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write meta data
            writer = self._write_meta_data(writer, meta)
            writer.writerow(["Found", len(data)])
            writer.writerow(["\n"])
            writer.writerow(["Index", "Sample", "Text", "Year", "Country", "Unmatch"])

            # Write data
            for idx, phrase in enumerate(data):
                # Check if PP and verbal discrepancy
                if self._search_phrase == "vosotros ":
                    lead_verb = meta["Leading verbs"][idx]["3ps_pl"]
                    follow_verb = meta["Following verbs"][idx]["3ps_pl"]
                elif self._search_phrase == "ustedes ":
                    lead_verb = meta["Leading verbs"][idx]["2ps_pl"]
                    follow_verb = meta["Following verbs"][idx]["2ps_pl"]
                else:
                    lead_verb = None
                    follow_verb = None

                if lead_verb is not None:
                    non_fit = "x"
                elif follow_verb is not None:
                    non_fit = "x"
                else:
                    non_fit = ""

                # Write data 1-indexed
                writer.writerow([idx+1,
                                 phrase['label'],
                                 phrase['text'],
                                 phrase['date'],
                                 phrase['country'],
                                 non_fit])

        return os.getcwd() + '/' + file_name

    def analyse(self, samples_list: list):
        """Analyse the given data according to basic statistical measures.
           Summation of general information, which means the total amount of
           samples, regarding a city from corpus.

        Args:
            samples_list (list): List of dictionaries with corpus data

        Returns:
            data (list): Retrieved data from PRESEEA
        """
        # Get total amount of samples for that city
        n_samples_city = self.retrieve_city_info()
        data = {'Total samples': n_samples_city}

        # Get the leading and following words for each search phrase
        data['Leading'] = [None]*len(samples_list)
        data['Following'] = [None]*len(samples_list)

        if type(samples_list) is not list:
            Warning("No samples list introduced! City might not be available.")
        else:
            classfier = WordClassifier("")
            for idx, sample in enumerate(samples_list):
                classfier.set_phrase(sample['text'])
                lead, follow = classfier.get_environment_words(self._search_phrase)
                data['Leading'][idx] = lead
                data['Following'][idx] = follow

        # Add basic meta information
        data['Name'] = self.get_author()

        # Update meta information regarding verbs
        data["Leading verbs"] = self.get_verbs(data['Leading'])
        data["Following verbs"] = self.get_verbs(data['Following'])

        return data

    def set_filter(self, city: str, gender: str,
                   age: str, education: str, phrase: str):
        self.set_city(city)
        self.set_gender(gender)
        self.set_age(age)
        self.set_education(education)
        self.set_search_phrase(phrase)

    def get_filter(self):
        city = 'City: {}'.format(self._city)
        gender = 'Gender: {}'.format(self._gender)
        age = 'Age: {}'.format(self._age)
        education = 'Education: {}'.format(self._education)

        return '{}, {}, {}, {}'.format(city, gender, age, education)

    def create_report(self, city: str, phrase: str):
        """Create a .csv file as a report for the
           phrases and their corresponding analysis
           based on the PRESEEA corpus data for
           the given city.

        Args:
            city (str): A city as feature in the corpus
            phrase (str): A phrase which has to be found
                in the corpus
        """
        # Define search issue with filters and phrase
        self.set_filter(city=city,
                        gender="all",  # "Hombre"
                        age="all",  # "Grupo 1"
                        education="all",  # "Bajo"
                        phrase=phrase)

        # Get data via scrapy framework as API
        sample_list = self.retrieve_phrase_data()

        # Get meta information from the retrieved data
        meta_data = self.analyse(sample_list)

        # Write data with stats into .csv file
        self.write_csv(data=sample_list,
                       meta=meta_data)
