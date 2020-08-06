AVAILABLE_CORPI = ['PRESEEA', 'CREA', 'COSER']


class Corpus:
    def __init__(self, name: str, author: str, search_phrase: str):
        if name not in AVAILABLE_CORPI:
            raise ValueError('Corpus not available!\
                Select from: {}'.format(AVAILABLE_CORPI))

        # Set class properties
        self._corpus_name = name
        if self._corpus_name == 'PRESEEA':
            self._address = 'https://preseea.linguas.net/Corpus.aspx'

        self._feature_dict = {}
        self._author = author
        self.set_search_phrase(search_phrase)

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

    def get_search_phrase(self) -> str:
        """Return instances' search phrase

        Returns:
            str: Corpus search phrase
        """
        return self._search_phrase

    def get_corpus_name(self):
        return self._corpus_name

    def get_author(self) -> str:
        """Get the name of the Corpus user

        Returns:
            str: Author name
        """
        return self._author

    def __repr__(self):
        print('Corpus: {}'.format(self._corpus_name))
