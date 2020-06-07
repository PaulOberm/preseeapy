from CorpusDefinition import Corpus
from CorpusPreseea import PRESEEA
from bs4 import BeautifulSoup

# corpus_1 = Corpus('PRESEEA')
# all_cities = corpus_preseea.get_all_cities()
# result = corpus_1.get_results()
# element = result.find_all('div', {"id": "divGrid"})

corpus_preseea = PRESEEA()
corpus_preseea.set_search_phrase('hago')
corpus_preseea.set_filter(city="Pereira", gender="Mujer", age="Grupo 1", education="Medio")

# TODO: Read correctly from CorpusDefinition request
test_list = corpus_preseea.retrieve_phrase_data()

corpus_preseea.write_csv("testfile.csv")