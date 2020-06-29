# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.shell import inspect_response


class PreseeabotSpider(scrapy.Spider):
    name = 'preseeabot'
    FIRST_NAME = "x"
    SURNAME = "x"
    INSTITUTION = "x"
    _education_key = "dnn$ctr520$TranscriptionQuery$chkFtStudyLevel$1"
    _age_key = "dnn$ctr520$TranscriptionQuery$chkFtAgeGroup$2"

    allowed_domains = ['preseea.linguas.net']
    start_urls = ['https://preseea.linguas.net/Corpus.aspx']
    _search_phrase = 'hago '

    # def __init__(self, phrase: str,
    #              city: str, gender: str,
    #              education: str, age: str):
    #     super().__init__()

    #     self._search_phrase = phrase
    #     self._city_key = self.map_to_city_key(city)
    #     self._gender_key = self.map_to_gender_key(city)
    #     self._education_key = self.map_to_education_key(city)
    #     self._age_key = self.map_to_age_key(city)

    def map_to_age_key(age: str) -> str:
        """Map an age class to the correct key for the PRESEEA webpage

        Args:
            age (str): Age classes (young, middle, old)

        Returns:
            str: Age class key in HTML webpage
        """

        if age == 'young':
            age_class = "dnn$ctr520$TranscriptionQuery$chkFtAgeGroup$1"
        elif age == 'middle':
            age_class = "dnn$ctr520$TranscriptionQuery$chkFtAgeGroup$2"
        elif age == 'old':
            age_class = "dnn$ctr520$TranscriptionQuery$chkFtAgeGroup$3"
        else:
            return ValueError('Unkown age class! \
                Available classes: young, middle, old.')

        return age_class

    def map_to_education_key(educaton: str) -> str:
        """Map an educaton class to the correct key for the PRESEEA webpage

        Args:
            educaton (str): Education classes (low, medium, high)

        Returns:
            str: Education class key in HTML webpage
        """

        if educaton == 'low':
            education_class = "dnn$ctr520$TranscriptionQuery$chkFtStudyLevel$1"
        elif educaton == 'medium':
            education_class = "dnn$ctr520$TranscriptionQuery$chkFtStudyLevel$2"
        elif educaton == 'high':
            education_class = "dnn$ctr520$TranscriptionQuery$chkFtStudyLevel$3"
        else:
            return ValueError('Unkown education class! \
                Available classes: low, medium, high.')

        return education_class

    def start_requests(self):
        """POST ASP.NET request with form data

        Yields:
            [scrapy.Request]: Request object to parse form response data
        """
        yield scrapy.Request(url=self.start_urls[0],
                             callback=self.parse_form)

    def parse_results(self, response):
        print(response)
        print(type(response))
        # Get table of responses from POST response
        phrase_table = response.css("table.preseea_grid")

        phrase_list = phrase_table.css("tr span").extract()
        phrase_list = [element for element in phrase_list if ('<span id=' and 'TextMatch') in element]

        NUM_ELEMENTS_PER_ITEM = 5

        # Iterate each table response
        for idx, phrase in enumerate(phrase_list):
            phrase = phrase.split("TextMatch")[1]
            # phrase = phrase.split("\r\n")[1]
            phrase = phrase.split("<span")[0] + " {} ".format(self._search_phrase) + phrase.split("</span>")[1].split("&lt")[0]

            date_info = phrase_table.css("tr td").extract()[2 + idx*NUM_ELEMENTS_PER_ITEM]
            country_info = phrase_table.css("tr td").extract()[3 + idx*NUM_ELEMENTS_PER_ITEM]

            yield {
                'text': phrase,
                'date': date_info.split("px;\">")[1].split('</td>')[0],
                'country': country_info.split("<td>")[1].split('</td>')[0],
            }

    def _prepare_DNN(self, dnn_string: str) -> dict:
        """Prepare a DNN for PRESEEA webpage

        Args:
            dnn_string (str): [description]

        Returns:
            dict: [description]
        """
        DNN = dnn_string.replace("`", '\'')
        DNN = DNN.replace("\'", "\"")
        DNN = DNN.replace("\\\'", "\"")
        DNN = DNN.replace("\\\"", "\"")
        DNN = DNN + "\""
        DNN = DNN.replace("\"", "\'")
        DNN = "\"" + DNN[1:]
        DNN = DNN[:-1] + "\""

        return DNN

    def parse_form(self, response):
        ScriptManager_TSM = ";;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en:16997a38-7253-4f67-80d9-0cbcc01b3057:ea597d4b:b25378d2"

        input_element_list = response.css('form input::attr(value)').extract()

        StylesheetManager_TSSM = input_element_list[2]
        EVENTTARGET = input_element_list[3]
        EVENTARGUMENT = input_element_list[4]
        VIEWSTATE = input_element_list[5]
        VIEWSTATEGENERATOR = input_element_list[6]
        VIEWSTATEENCRYPTED = input_element_list[7]
        EVENTVALIDATION = input_element_list[8]
        SEARCH = input_element_list[9]
        SHOW = input_element_list[11]
        DNN = self._prepare_DNN(input_element_list[12])

        # Set up form with generative keys
        formdata = {"StylesheetManager_TSSM": StylesheetManager_TSSM,
                    "ScriptManager_TSM": ScriptManager_TSM,
                    "__EVENTTARGET": EVENTTARGET,
                    "__EVENTARGUMENT": EVENTARGUMENT,
                    "__VIEWSTATE": VIEWSTATE,
                    "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
                    "__VIEWSTATEENCRYPTED": VIEWSTATEENCRYPTED,
                    "__EVENTVALIDATION": EVENTVALIDATION,
                    "dnn$ctr520$TranscriptionQuery$txtFirstname": self.FIRST_NAME,
                    "dnn$ctr520$TranscriptionQuery$txtSurname": self.SURNAME,
                    "dnn$ctr520$TranscriptionQuery$txtInstitution": self.INSTITUTION,
                    "dnn$ctr520$TranscriptionQuery$chkFtCity$1": "on",
                    "dnn$ctr520$TranscriptionQuery$chkFtSex$2": "on",
                    self._age_key: "on",
                    self._education_key: "on",
                    "dnn$ctr520$TranscriptionQuery$txtFtValue": self._search_phrase,
                    "dnn$ctr520$TranscriptionQuery$btnFtSearch": SEARCH,
                    "dnn$ctr520$TranscriptionQuery$hdnShowPagerResults": "",
                    "dnn$ctr520$TranscriptionQuery$hdnPagerIndex": "",
                    "dnn$ctr520$TranscriptionQuery$summary1$txtValidatorHack": "",
                    "dnn$ctr520$TranscriptionQuery$summary1$hdnReShow": SHOW,
                    "ScrollTop": "536",
                    "__dnnVariable": DNN}

        yield scrapy.FormRequest(url=self.start_urls[0],
                                 formdata=formdata,
                                 callback=self.parse_results)

# instance = PreseeabotSpider()

# test = instance.start_requests()

# print('test')