import pandas as pd
import requests
import urllib.request

AVAILABLE_CORPI = ['PRESEEA', 'CREA', 'COSER']


class Corpus:
    def __init__(self, name: str):
        if name not in AVAILABLE_CORPI:
            raise ValueError('Corpus not available! Select from: {}'.format(AVAILABLE_CORPI))

        # Set class properties
        self._corpus_name = name
        if self._corpus_name == 'PRESEEA':
            self._address = 'https://preseea.linguas.net/Corpus.aspx'

        self._feature_dict = {}

    def get_corpus_name(self):
        return self._corpus_name

    def __repr__(self):
        print('Corpus: {}'.format(self._corpus_name))
