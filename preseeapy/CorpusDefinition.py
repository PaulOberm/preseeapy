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

        self._feature_dict = []
        self._city = ""
        self._gender = ""
        self._age = ""
        self._education = ""

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
        else:
            raise ValueError('Given location or city: \
                {} is not defined'.format(name))

    def set_sex(self, name: str):
        """Set Corpus' instance gender by its name and check beforehand

        Args:
            name (str): Name of the gender the corpus should be filtered on
        """
        sex_list = self._feature_dict['Sex']
        if name in sex_list:
            self._gender = name
        else:
            Warning('Gender not in accordance with corpus')
            self._gender = name

    def set_age(self, name: str):
        """Set Corpus' instance age by its name and check beforehand

        Args:
            name (str): Name of the age the corpus should be filtered on
        """
        age_list = self._feature_dict['Age']
        if name in age_list:
            self._age = name
        else:
            Warning('Age definition not in accordance with corpus')
            self._age = name

    def set_education(self, name: str):
        """Set Corpus' instance education by its name and check beforehand

        Args:
            name (str): Name of the education the corpus should be filtered on
        """
        education_list = self._feature_dict['Education']
        if name in education_list:
            self._education = name
        else:
            Warning('Education definition not in accordance with corpus')
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
        countries = [country for country in self._feature_dict["Country"].keys()]

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

    def _check_cities(self, sample: str) -> list:
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

    def prepare_post_data(self, initial: bool) -> dict:
        """This functions prepares a raw text file for PRESEEA post request

        Returns:
            dict: post data as dictionary
        """

        with open('test.html') as raw_request:
            content = raw_request.read()
            name_list = content.split("form-data; name=")[1:]

            data = {}
            # For ASP.NET pages, primarily retrieve __VIEWSTATE
            if initial:
                name_list = name_list[8:]

            for name in name_list:
                temporary_list = name.split("\\r\\n")
                name = temporary_list[0][1:-1]
                value = temporary_list[2]

                data[name] = value

        if not initial:
            with open('requestdata.txt') as previous_request:
                content = previous_request.read()
                data["__VIEWSTATE"] =  content.split('name="__VIEWSTATE" id="__VIEWSTATE" value="')[1].split(' />\\r\\n</div>\\r\\n\\r\\n<script')[0][:-1]
                data["__EVENTVALIDATION"] = content.split('name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="')[1].split(' />\\r\\n</div><script')[0][:-1]

        return data

    def get_results(self):
        values_inital = self.prepare_post_data(initial=True)
        initial_response = requests.post(self._address, params=values_inital, headers=self._headers)
        with open("requestdata.txt", "w") as f:
            # Extract curl request here into text file!!!!!!!!
            f.write(str(initial_response.content))

        values = self.prepare_post_data(initial=False)
        session = requests.Session()
        response = session.post(self._address, params=values, headers=self._headers)
        with open("requests_results.html", "w") as f:
            f.write(response.content.decode("utf-8") )


        # TODO: Response does not contain whished data
        soup = BeautifulSoup(content, 'lxml')
        return soup

    def __repr__(self):
        print('Corpus: {}'.format(self._corpus_name))
        print('Filter:\n{}'.format(self.get_filter()))
