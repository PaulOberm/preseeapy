import unittest
from preseeapy.utils import ProcessHandler


class TestUtilsClass(unittest.TestCase):
    def test_ProcessHandler(self):
        self.assertRaises(ValueError, ProcessHandler, 5)
