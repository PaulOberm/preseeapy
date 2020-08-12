from .WordClassifier import WordClassifier


class VerbClassifier():
    gerundium_list = ['iendo']

    def __init__(self, word_list: list):
        self._word_classifier = WordClassifier("")
        self.set_word_list(word_list)

    def set_phrase(self, phrase: str):
        """Set string type phrase as word list

        Args:
            phrase (str): Phrase to be set as word list
        """
        self._word_classifier.set_phrase(phrase)
        word_list = self._word_classifier.get_word_list()
        self.set_word_list(word_list)

    def get_environment_verbs(self, word: str) -> (list, list):
        """Get environmental verbs around a search phrase

        Args:
            word (str): Search phrase as word

        Returns:
            list: List of dictionaries
        """
        lead_words, follow_words = self._word_classifier.get_environment_words(word)

        return_list = []
        for word_list in [lead_words, follow_words]:
            self.set_word_list(word_list)
            classified_words = self.classify_verbs()
            return_list.append(classified_words)

        return return_list[0], return_list[1]

    def set_word_list(self, word_list: list):
        """Set the class instances list of words.
           List is checked by type beforehand.

        Args:
            word_list (list): Input list of possible words
        """
        checked_list = []
        for word in word_list:
            if type(word) != str:
                continue
            if len(word) < 2:
                continue
            if (word[-1] == "?" or word[-1] == "!"):
                word = word[:-1]
            if (word[0] == "¿" or word[0] == "¡"):
                word = word[1:]

            checked_list.append(word)

        self._word_list = checked_list

    def get_word_list(self) -> list:
        return self._word_list

    def _check_verb(func):
        def wrapper(self, word: str) -> bool:
            ending_list, exception_list = func(self, word)

            is_verb_class = False
            if word in exception_list:
                is_verb_class = False
            elif self._word_has_ending(word, self.gerundium_list):
                # If given word is a gerundium, no verb
                is_verb_class = False
            else:
                # If word ends with those endings, it belongs to that class
                is_verb_class = self._word_has_ending(word, ending_list)

            return is_verb_class
        return wrapper

    def _word_has_ending(self, word: str, ending_list: list) -> bool:
        """Check if a given word ends with a string in the ending list

        Args:
            word (str): Word to be checked
            ending_list (list): Available endings to be classified
                as a verb of a specific class

        Returns:
            bool: Word belongs to a class defined by endings
        """
        for ending in ending_list:
            width = len(ending)

            if ending in word[-width:]:
                has_ending = True
                break
        else:
            has_ending = False

        return has_ending

    @_check_verb
    def is_1person_singular(self, word: str) -> bool:
        """Check if a word is a verb in 1. person, singular

        Args:
            word (str): Single word

        Returns:
            bool: Is 1P, SG
        """
        ending_list = ['o', 'oy']
        exception_list = [' no ', ' lo', 'bueno',
                          'pero', 'cómo']

        return ending_list, exception_list

    @_check_verb
    def is_2person_singular(self, word: str) -> bool:
        """Check if a word is a verb in 2. person, singular

        Args:
            word (str): Single word

        Returns:
            bool: Is 2P, SG
        """
        ending_list = ['as', 'es']
        exception_list = [' les ', 'cosas', 'bases']

        return ending_list, exception_list

    @_check_verb
    def is_3person_singular(self, word: str) -> bool:
        """Check if a word is a verb in 3. person, singular

        Args:
            word (str): Single word

        Returns:
            bool: Is 3P, SG
        """
        ending_list = ['e', 'a']
        exception_list = [' les ', ' le ', ' la ', ' las', 'que', 'se', 'la']

        return ending_list, exception_list

    @_check_verb
    def is_1person_plural(self, word: str) -> bool:
        """Check if a word is a verb in 1. person, plural

        Args:
            word (str): Single word

        Returns:
            bool: Is 1P, PL
        """
        ending_list = ['mos', 'monos']
        exception_list = [' monos ']

        return ending_list, exception_list

    @_check_verb
    def is_2person_plural(self, word: str) -> bool:
        """Check if a word is a verb in 2. person, plural

        Args:
            word (str): Single word

        Returns:
            bool: Is 2P, PL
        """
        ending_list = ['eis', 'ois', 'ais', 'áis', 'éis']
        exception_list = []

        return ending_list, exception_list

    @_check_verb
    def is_3person_plural(self, word: str) -> bool:
        """Check if a word is a verb in 3. person, plural

        Args:
            word (str): Single word

        Returns:
            bool: Is 3P, PL
        """
        ending_list = ['en', 'on', 'an', 'án']
        exception_list = ['con', 'en']

        return ending_list, exception_list

    def classify_verbs(self) -> dict:
        """This method classfies a list of words according
           their form in their personal conjugation, if it is a verb

        Returns:
            dict: Sorted verbs from a list of words
        """

        verb_class = {
                "1ps_sg": [],
                "2ps_sg": [],
                "3ps_sg": [],
                "1ps_pl": [],
                "2ps_pl": [],
                "3ps_pl": [],
            }

        for word in self._word_list:
            if self.is_1person_singular(word):
                verb_class["1ps_sg"].append(word)
            if self.is_2person_singular(word):
                verb_class["2ps_sg"].append(word)
            if self.is_3person_singular(word):
                verb_class["3ps_sg"].append(word)
            if self.is_1person_plural(word):
                verb_class["1ps_pl"].append(word)
            if self.is_2person_plural(word):
                verb_class["2ps_pl"].append(word)
            if self.is_3person_plural(word):
                verb_class["3ps_pl"].append(word)

        return verb_class
