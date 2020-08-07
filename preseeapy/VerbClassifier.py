class VerbClassifier():
    def __init__(self, word_list: str):
        self.set_word_list(word_list)

    def set_word_list(self, word_list: str):
        self._word_list = word_list

    def _check_verb(func):
        def wrapper(self, word: str) -> bool:
            ending_list, exception_list = func(self, word)

            is_verb_class = False
            if word in exception_list:
                is_verb_class = False
            else:
                for ending in ending_list:
                    width = len(ending)
                    if len(word)>1 and (word[-1]=="?" or word[-1]=="!"):
                        word = word[:-1]

                    if ending in word[-width:]:
                        is_verb_class = True
                        break
            return is_verb_class
        return wrapper

    @_check_verb
    def is_1person_singular(self, word: str) -> bool:
        """Check if a word is a verb in 1. person, singular

        Args:
            word (str): Single word

        Returns:
            bool: Is 1P, SG
        """
        ending_list = ['o', 'oy']
        exception_list = [' no ', ' lo']

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
        exception_list = [' les ']

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
        exception_list = [' les ', ' le ', ' la ', ' las']

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
        ending_list = ['en', 'on', 'an']
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
