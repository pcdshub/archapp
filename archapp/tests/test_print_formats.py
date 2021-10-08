import unittest

from archapp import print_formats


def test_print_list_no_crash():
    print_formats.list_print([], do_print=False)
    print_formats.list_print(["text"], do_print=False)
    print_formats.list_print(["text"] * 50, do_print=False)
