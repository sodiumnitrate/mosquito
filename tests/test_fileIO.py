"""
Unit tests for the fileIO submodule.
"""

from mosquito.fileIO import *

class TestFileIO:
    def test_file_len(self):
        n = file_len("aux_files/test.dat")
        assert n == 6

    def test_tail(self):
        tail_str = tail("aux_files/test.dat", n=2)
        assert len(tail_str) == 2
        assert "potato" in tail_str[-1]

    def test_check_if_end_of_file_contains(self):
        assert check_if_end_of_file_contains("aux_files/test.dat", "potato")
        assert not check_if_end_of_file_contains("aux_files/test.dat", "refrigerator")