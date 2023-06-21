"""
Consistency checks for the functions of mosquito.string_print.
"""
from mosquito.string_print import *

class TestStringPrint:
    def test_color_char(self):
        char = "A"
        res = color_char(char)
        assert len(res) > len(char)

    def test_color_string_with_ranges(self):
        test_string = "LOREMIPSUMDOLOR"
        ranges = [(2,4), (6,7)]

        res = color_string_with_ranges(test_string, ranges)

        assert len(res) > len(test_string)

    def test_color_string_with_ranges_2(self):
        test_string = "LOREMIPSUMDOLOR_LIPSUMMM"
        ranges = [[(2,4), (6,7)], [(8,10)]]

        res = color_string_with_ranges(test_string, ranges)

        assert len(res) > len(test_string)

    def test_color_string_with_ranges_3(self):
        test_string = "LOREMIPSUMDOLOR_LIPSUMMM"
        ranges = (5,10)

        res = color_string_with_ranges(test_string, ranges)

        assert len(res) > len(test_string)