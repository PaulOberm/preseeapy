import unittest
from preseeapy.ASPXTwister import ASPXTwisterClass
from preseeapy.preseeaspider.spiders.preseeabot import PreseeabotSpider


class TestASPXTwisterClass(unittest.TestCase):
    def setUp(self):
        self.parameter_dict = {"filter_1": "test",
                               "filter_2": "test"}
        self.twister_instance = ASPXTwisterClass(self.parameter_dict,
                                                 PreseeabotSpider)

    def test_check_parameters(self):
        """Check if the parameter dictionary with the filters has
           the correct format
        """
        checked = self.twister_instance.check_parameters()

        self.assertEqual(True, checked)

    def test_get_parameters(self):
        """Test if the filters are correctly unchanged from the input
           as object property
        """
        object_parameters = self.twister_instance.get_parameters()

        self.assertEqual(object_parameters["filter_1"],
                         self.parameter_dict["filter_1"])
