from CorpusDefinition import Corpus
from CorpusPreseea import PRESEEA
from bs4 import BeautifulSoup
from scrapy.downloadermiddlewares import httpproxy
from preseeaspider.spiders.preseeabot import PreseeabotSpider

# Get PreseeabotSpider object
preseeabot = PreseeabotSpider()
data = preseeabot.start_requests()
# TODO: How to execute request object
response = next(data)

# preseea_downloader = httpproxy.HttpProxyMiddleware()
# test = preseea_downloader.process_request(response, preseeabot)

corpus_preseea = PRESEEA()
corpus_preseea.set_search_phrase('hago ')
corpus_preseea.set_filter(city="Pereira", gender="Mujer", age="Grupo 1", education="Medio")

# TODO: Read correctly from CorpusDefinition request
test_list = corpus_preseea.retrieve_phrase_data()

corpus_preseea.write_csv("testfile.csv")