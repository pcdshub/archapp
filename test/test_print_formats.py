import unittest
from archapp.util import print_formats

class PrintFormatsTestCase(unittest.TestCase):
    def test_print_list_no_crash(self):
        print_formats.list_print([], do_print=False)
        print_formats.list_print(["text"], do_print=False)
        print_formats.list_print(["text"] * 50, do_print=False)
