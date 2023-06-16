from mosquito.mosquito import *

import pdb

class TestMosquito:
    def test_check_range_overlap(self):
        range_1 = (5,55)
        range_2 = (1,20)

        assert check_range_overlap(range_1, range_2)

        range_1 = (1,20)
        range_2 = (25,30)

        assert not check_range_overlap(range_1, range_2)

    def test_ranges_from_idx_list(self):
        idx = [2, 3, 4, 5, 55, 56, 57, 58]
        ranges = ranges_from_idx_list(idx)

        assert len(ranges) == 2
        assert ranges[0][0] == 2
        assert ranges[0][1] == 5
        assert ranges[1][0] == 55
        assert ranges[1][1] == 58

    def test_ranges_from_idx_list_2(self):
        idx = [2, 3, 4, 5, 55]
        ranges = ranges_from_idx_list(idx)

        assert len(ranges) == 2
        assert ranges[0][0] == 2
        assert ranges[0][1] == 5
        assert ranges[1][0] == 55
        assert ranges[1][1] == 55

    def test_ranges_from_idx_list_3(self):
        idx = [2, 55]
        ranges = ranges_from_idx_list(idx)

        assert len(ranges) == 2
        assert ranges[0][0] == 2
        assert ranges[0][1] == 2
        assert ranges[1][0] == 55
        assert ranges[1][1] == 55

        idx = [2, 55, 56]
        ranges = ranges_from_idx_list(idx)

        assert len(ranges) == 2
        assert ranges[0][0] == 2
        assert ranges[0][1] == 2
        assert ranges[1][0] == 55
        assert ranges[1][1] == 56

    def test_ranges_from_idx_list_2(self):
        idx = [2]
        ranges = ranges_from_idx_list(idx)

        assert len(ranges) == 1
        assert ranges[0][0] == 2
        assert ranges[0][1] == 2

        idx = []
        ranges = ranges_from_idx_list(idx)
        assert len(ranges) == 0

    def test_array_contains_n_consecutive_vals(self):
        y = [0,0,0,5,5,5,2,2,0,0,0,0]
        assert array_contains_n_consecutive_vals(y, 0, 3)
        assert not array_contains_n_consecutive_vals(y, 5, 4)
        assert not array_contains_n_consecutive_vals(y, 2, 3)
        assert not array_contains_n_consecutive_vals(y, 10, 2)

    def test_sparse_array_for_plot(self):
        y = [0,5,5,5,5,0,0,0,0,0,0,5,5,5,5,5,5,0,0,0,0,0,0,5,5,5,5,5,0,0,0,0,0]
        x = list(range(0,len(y)))
        new_x, new_y = sparse_array_for_plot(x, y)

        assert len(new_x) == len(new_y)

        assert not array_contains_n_consecutive_vals(new_y, 0, 3)