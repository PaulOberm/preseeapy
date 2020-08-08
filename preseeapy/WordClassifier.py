class WordClassifier():
    def __init__(self, phrase: str):
        self.NO_WORD_LIST = ["", "/", "…"]

        # Environmental words range
        self.WORD_RANGE = 3
        self._word_list = self.set_word_list(phrase)

    def set_phrase(self, phrase: str):
        self._word_list = self.set_word_list(phrase)

    def get_word_list(self):
        return self._word_list

    def _is_word(self, word: str) -> bool:
        """This method checks if a string is a word

        Args:
            word (str): String to be checked

        Returns:
            bool: Is string a word
        """
        is_word = False
        if word not in self.NO_WORD_LIST:
            is_word = True

        return is_word

    def set_word_list(self, phrase: str) -> list:
        """Get a list of words from a complete phrase as string

        Args:
            phrase (str): Complete string describing a phrase

        Returns:
            list: List of single words within a phrase
        """
        word_list = phrase.split(" ")
        word_list = [word for word in word_list if self._is_word(word)]

        return word_list

    def get_leading_words(self, search_phrase: str) -> list:
        """Get a number of leading words from phrase in
           front of a search phrase

        Returns:
            list: Frontal words
        """
        search_phrase = search_phrase.replace(" ", "")
        phrase_idx = self._word_list.index(search_phrase)
        sub_list = self._word_list[:phrase_idx]

        if len(sub_list) > self.WORD_RANGE:
            leading_list = sub_list[-self.WORD_RANGE:]
        else:
            leading_list = sub_list

        return leading_list

    def get_following_words(self, search_phrase: str) -> list:
        """Get a number of following words from phrase
           after a search phrase

        Returns:
            list: Posterior words
        """
        search_phrase = search_phrase.replace(" ", "")
        phrase_idx = self._word_list.index(search_phrase)
        sub_list = self._word_list[phrase_idx+1:]

        if len(sub_list) > self.WORD_RANGE:
            following_list = sub_list[:self.WORD_RANGE]
        else:
            following_list = sub_list

        return following_list

    def get_environment_words(self, search_phrase: str) -> (list, list):
        """Get leading and following words from phrase
           around the search phrase.

        Arguments:
            str: Phrase within phrase to search words around it

        Returns:
            list: List of leading words
            list: List of following words
        """
        # Get environmental words
        leading_words = self.get_leading_words(search_phrase)
        following_words = self.get_following_words(search_phrase)

        return leading_words, following_words
