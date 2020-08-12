from twisted.internet import reactor
from multiprocessing import Queue
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy import signals
import scrapy


class ASPXTwisterClass():
    def __init__(self, parameters: dict, spider: scrapy.Spider):
        self._crawler_meta = {
            'USER_AGENT': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                           (KHTML, like Gecko) Chrome/55.0.2883.75 \
                           Safari/537.36",
            'DOWNLOAD_TIMEOUT': 100,
            'REDIRECT_ENABLED': False,
            'SPIDER_MIDDLEWARES': {
                'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': True
            }
        }

        # Save crawled results iteratively within a list
        self._crawler_results = []
        self.set_parameters(parameters)
        self._spider_bot = spider

    # Signal process function definition
    def crawler_results(self, signal, sender, item, response, spider):
        self._crawler_results.append(item)

    def _retrieve_phrase_data_subprocess(self, queue: Queue) -> list:
        """This method retrieves a list of phrases from an html document

        Returns:
            list: List of strings with phrases containing searched phrase
        """
        # Set up a crawler process to use a spider
        runner = CrawlerRunner(self._crawler_meta)

        # Middleware between downloader and spider
        dispatcher.connect(self.crawler_results, signal=signals.item_passed)
        dispatcher.connect(reactor.stop, signal=signals.spider_closed)

        # Apply requests from spider - Add arguments to initialize the spider
        if self.check_parameters():
            try:
                defered = runner.crawl(self._spider_bot,
                                       self._parameter_dict)

                defered.addBoth(lambda _: reactor.stop())

                reactor.run()
                queue.put(self._crawler_results)
            except Exception as e:
                queue.put(e)
        else:
            queue.put(None)

    def set_parameters(self, parameters: dict):
        self._parameter_dict = parameters

    def get_parameters(self) -> dict:
        return self._parameter_dict

    def check_parameters(self):
        """Check the given filter parameters for a POST request.

        Returns:
            bool: Is every filter set to post request
        """
        keys = list(self._parameter_dict.keys())

        # Check all filters for availability
        check_filters = True
        for filter_name in keys:
            if self._parameter_dict[filter_name] == "":
                check_filters = False

        return check_filters
