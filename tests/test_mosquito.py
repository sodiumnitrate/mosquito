from mosquito.mosquito import *

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

    def test_get_number_of_zeros_after_decimal(self):
        number = 0.99
        assert get_number_of_zeros_after_decimal(number) == 0

        number = -0.099
        assert get_number_of_zeros_after_decimal(number) == 1

        number = 1.55
        caught = False
        try:
            get_number_of_zeros_after_decimal(number)
        except ValueError:
            caught = True

        assert caught

        number = 0.0000055
        assert get_number_of_zeros_after_decimal(number) == 5

    def test_is_num_in_range(self):
        num = 55
        range_1 = (55, 105)
        assert is_num_in_range(num, range_1)

        num = 65.2
        assert is_num_in_range(num, range_1)

        num = 105
        assert is_num_in_range(num, range_1)

    def test_check_overlap_range_list(self):
        ranges = [(1,5), (10, 20), (55.5, 123.3)]
        assert not check_overlap_range_list(ranges)

        ranges = [(1, 15), (10, 20), (55.5, 123.3)]
        assert check_overlap_range_list(ranges)

        ranges = [(1, 10), (10, 20), (55.5, 123.3)]
        assert check_overlap_range_list(ranges)

    def test_check_overlap_range_two_lists(self):
        ranges_1 = [(1,5), (10, 20), (55.5, 123.3)]
        ranges_2 = [(1,5), (10, 60), (55.5, 123.3)]
        assert check_overlap_range_two_lists(ranges_1, ranges_2)

        ranges_1 = [(1,5), (10, 15), (300, 400)]
        ranges_2 = [(6,8), (20, 60), (55.5, 123.3)]
        assert not check_overlap_range_two_lists(ranges_1, ranges_2)

    def test_check_overlap_range_list_of_lists(self):
        ranges_1 = [(1,5), (10, 15), (300, 400)]
        ranges_2 = [(6,8), (20, 60), (55.5, 123.3)]
        ranges_3 = [(-100, 0), (800, 900.33)]

        list_of_ranges = [ranges_1, ranges_2, ranges_3]
        assert not check_overlap_range_list_of_lists(list_of_ranges)

    def test_sort_array_by_column(self):
        a = [1,0,3,2,4]
        b = [0,1,2,3,4]

        data = [a, b]

        sorted_data = sort_arrays(a, b)
        
        a_sorted = sorted_data[0]
        b_sorted = sorted_data[1]

        assert a_sorted == b
        assert b_sorted == a

        c = [5,6,7,8,9]

        sorted_data = sort_arrays(a, [b, c])

        assert sorted_data[0] == b
        assert sorted_data[1] == a
        assert sorted_data[2] == [6, 5, 8, 7, 9]