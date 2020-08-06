class CityCorpusMixin():
    # def __init__(self):
    #     self._city = ""

    def set_city(self, name: str):
        """Set Corpus' instance city by its name and check beforehand

        Args:
            name (str): Name of the city the corpus should be filtered on
        """
        city_list = list(self._feature_dict['City'].keys())
        if name in city_list:
            self._city = name
        elif name == "all":
            self._city = "all"
        else:
            Warning('Given location or city: \
                {} is not defined'.format(name))
            self._city = ""

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

    def retrieve_city_info(self) -> int:
        """Get general information about a city.

        Args:
            n_total (int): Total number of samples for a city
        """
        city_list = list(self._feature_dict['City'].keys())
        if self._city not in city_list:
            Warning('City not available in Corpus.')
            return None

        # Number of samples per city
        n_total = self.get_number_city_samples()

        return n_total

    def get_number_city_samples(self) -> int:
        """Get number of available samples for a city.

        Returns:
            n_total (int): Total number of samples for a city
        """
        # Temporarily save search phrase
        temp_search_phrase = self._search_phrase
        # Use empty search phrase to get available samples
        self._search_phrase = " "

        # Get number of samples for that phrase
        n_total = self.get_number_samples()

        # Set back correct search phrase
        self._search_phrase = temp_search_phrase

        return n_total

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

    def __str__(self):
        return "city:{}".format(self._city)
