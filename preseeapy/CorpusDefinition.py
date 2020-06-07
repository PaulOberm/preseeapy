import pandas as pd
import requests
import itertools as it
import urllib.request
from bs4 import BeautifulSoup

AVAILABLE_CORPI = ['PRESEEA', 'CREA', 'COSER']


class Corpus:
    def __init__(self, name: str):
        if name not in AVAILABLE_CORPI:
            raise ValueError('Corpus not available! Select from: {}'.format(AVAILABLE_CORPI))
        
        # Set class properties
        self._corpus_name = name
        if self._corpus_name == 'PRESEEA':
            self._address = 'https://preseea.linguas.net/Corpus.aspx'
        
        self._feature_list = []
        self._city = ""
        self._gender = ""
        self._age = ""
        self._education = ""

        self._headers = headers = {
                    'authority': 'preseea.linguas.net',
                    'cache-control': 'max-age=0',
                    'upgrade-insecure-requests': '1',
                    'origin': 'https://preseea.linguas.net',
                    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary0KA5113AdN33RDmf',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': 'https://preseea.linguas.net/Corpus.aspx',
                    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cookie': '.ASPXANONYMOUS=FZLZtxBx1gEkAAAAY2VlNzIxYzQtYmQ0MC00ZjY5LTk0ZDItMTRkMTk5YzIxOGNk0; 51D=3155378975999999999; language=es-ES',
                    }

        # Request workaround
        with open('example.txt', 'r') as text:
            self._data = text.read()
    
    def get_corpus_name(self):
        return self._corpus_name
    
    def set_city(self, name: str):
        """Set Corpus' instance city by its name and check beforehand

        Args:
            name (str): Name of the city the corpus should be filtered on
        """
        city_list = self.get_all_cities()
        if name in city_list:
            self._city = name
    
    def set_sex(self, name: str):
        """Set Corpus' instance gender by its name and check beforehand

        Args:
            name (str): Name of the gender the corpus should be filtered on
        """
        sex_list = self._feature_list['Sex']
        if name in sex_list:
            self._gender = name
    
    def set_age(self, name: str):
        """Set Corpus' instance age by its name and check beforehand

        Args:
            name (str): Name of the age the corpus should be filtered on
        """
        age_list = self._feature_list['Age']
        if name in age_list:
            self._age = name
    
    def set_education(self, name: str):
        """Set Corpus' instance education by its name and check beforehand

        Args:
            name (str): Name of the education the corpus should be filtered on
        """
        education_list = self._feature_list['Education']
        if name in education_list:
            self._education = name

    def set_filter(self, city: str, gender: str, age: str, education: str):
        self.set_city(city)
        self.set_sex(gender)
        self.set_age(age)
        self.set_education(education)

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
        countries = [country for country in self._feature_list["Country"].keys()]

        return countries

    
    def get_all_cities(self) -> list:
        """Return all the available cities in the Corpus

        Returns:
            list: List of strings with the city names
        """

        temporary_city_list = []
        for country in self.get_corpus_countries():
            temporary_city_list.append(self._feature_list["Country"][country])

        city_list = list(it.chain.from_iterable(temporary_city_list))

        return city_list


    def _check_cities(self, sample: str) -> list:
        """Check if samples are available for that feature

        Args:
            sample (str): Sample name, e.g. Colombia

        Returns:
            list: List of strings with available samples
        """
        # Get available samples for feature
        sample_list = self.get_corpus_countries()

        # Compare demanded sample with the available feature list
        try:
            feature_list = self._feature_list["Country"][sample]
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
        city_list = self._check_cities(country)

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

    def get_results(self):
        response = requests.post(self._address, headers=self._headers, data=self._data)
        response = urllib.request.urlopen(self._address)
        req = urllib.request.Request(self._address, data=data, headers=self._headers)

        content = response.read()

        # TODO: Response does not contain whished data
        soup = BeautifulSoup(content, 'lxml')
        return soup

    def __repr__(self):
        print('Corpus: {}'.format(self._corpus_name))
        print('Filter:\n{}'.format(self.get_filter()))
