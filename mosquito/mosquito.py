import numpy as np
import subprocess
from statistics import mean
from itertools import combinations

from mosquito.type_check import is_one_d_int_array, is_one_d_array, is_one_d_num_array


def get_running_job_list(user_name):
    '''
    Function to get list of jobs (in any status) by the given user. Designed to
    be used on Yale's Grace cluster, it may not work on any arbitrary system
    running Slurm.
    '''
    job_list = subprocess.check_output(['squeue', '-u', user_name]).split()
    job_id = []
    for field in job_list:
        field_str = str(field)[2:-1]
        if len(field_str) == 8 and field_str.isnumeric():
            print(field_str)
            job_id.append(field_str)

    return job_id

def add_dicts(dict1, dict2):
    """
    Function that adds two dictionaries with identical keys such that
    the values corresponding to the same key get added.
    """
    # adds together values in dicts given the keys are exactly the same
    assert (dict1.keys() == dict2.keys())

    for key in dict1.keys():
        dict1[key] += dict2[key]

    return dict1

def movmean(nums, window=5):
    """Function that calculates the moving mean of a list of numbers."""
    # implement a simple moving mean
    assert (window > 0)
    assert (isinstance(window, int))

    # check if nums is a list of numbers
    if np.isscalar(nums):
        print("ERROR: you must provide a list or array of numbers for calculating moving mean.")
        return None

    # determine radius
    if window % 2 != 0:
        left_r = window // 2
        right_r = window // 2
    else:
        # matlab style
        left_r = window // 2
        right_r = window // 2 - 1

    averaged = []
    for i in range(len(nums)):
        start = max(i - left_r, 0)
        end = min(i + right_r, len(nums))

        averaged.append(mean(nums[start:end + 1]))

    return averaged

def check_range_overlap(range_1, range_2):
    """
    Given two ranges (a,b) and (c,d), return True if they overlap.
    """

    if isinstance(range_1, tuple) or isinstance(range_1, list):
        n = len(range_1)
        if n != 2:
            print("ERROR: range_1 contains {n} elements.")
            return
    else:
        print("ERROR: range_1 must be a tuple or a list of two elements.")
        return

    if isinstance(range_2, tuple) or isinstance(range_2, list):
        n = len(range_2)
        if n != 2:
            print("ERROR: range_1 contains {n} elements.")
            return
    else:
        print("ERROR: range_1 must be a tuple or a list of two elements.")
        return

    a, b = range_1[0], range_1[1]
    c, d = range_2[0], range_2[1]

    if d < a or c > b:
        return False
    return True

# TODO: refactor the following 3 
def check_overlap_range_list_of_lists(list_of_lists):
    """
    Given a list of list of ranges, check overlap across sublists.
    """
    res = combinations(list_of_lists, 2)
    for pair in res:
        if check_overlap_range_two_lists(pair[0], pair[1]):
            return True

    return False

def check_overlap_range_two_lists(list_1, list_2):
    """
    Given two list of ranges, return True if there is any overlap,
    Fale if there is none.
    """
    for range_1 in list_1:
        for range_2 in list_2:
            if check_range_overlap(range_1, range_2):
                return True

    return False

def check_overlap_range_list(list_1):
    """
    Given a list of ranges, return True if any overlap, False if not.
    """
    for i in range(len(list_1)):
        for j in range(i+1, len(list_1)):
            if check_range_overlap(list_1[i], list_1[j]):
                return True

    return False

def merge_dicts(dict1, dict2):
    """
    Function that merges two dicts such that:
    - if a key exists in both, the corresponding values are added
    - if a key does not exist in both, it gets added to the final dict
      without any manip of the value
    """
    new_dict = {}
    for key, val in dict1.items():
        new_dict[key] = val

    for key, val in dict2.items():
        if key in new_dict.keys():
            new_dict[key] += val
        else:
            new_dict[key] = val

    return new_dict

def ranges_from_idx_list(idx):
    """
    Given a list of indices, get a list of ranges (in the form of tuples)
    of contiguous pieces.

    E.g.: 
    input --> idx = [2,3,4,5,55,56,57,58]
    output --> [(2,5), (55,58)]
    """
    if not is_one_d_int_array(idx):
        print("ERROR: idx must be a 1-d integer array.")
        raise TypeError

    n = len(idx)

    if n == 1:
        return [(idx[0],idx[0])]
    elif n == 0:
        return []

    ranges = []
    curr = 0
    prev = None
    while curr < n:
        if prev is None:
            start = idx[curr]
            prev = curr
            curr += 1
            continue
        if idx[curr] > idx[prev] + 1:
            end = idx[prev]
            ranges.append((start, end))
            start = idx[curr]

        prev = curr
        curr += 1

    if start > ranges[-1][1]:
        end = idx[-1]
        ranges.append((start, end))

    return ranges

def sparse_array_for_plot(x, y):
    """
    Given a data of the form f(x)=y, if y is very large, it's hard to plot. But if
    y contains large regions of zeros, these could be removed to improve plot performance.

    AFAIK, there's no built-in matplotlib functionality that achieves this.
    """
    if not is_one_d_array(x):
        print("ERROR: x not a 1-d array.")
        raise TypeError
    if not is_one_d_array(y):
        print("ERROR: y not a 1-d array.")
        raise TypeError
    if len(x) != len(y):
        print("ERROR: x and y must be of the same length.")
        return None

    idx = np.where(np.array(y) == 0)[0]
    ranges = ranges_from_idx_list(idx)
    ranges = [r for r in ranges if r[1] - r[0] + 1 > 2]
    indices_to_keep = []
    start = 0
    for r in ranges:
        indices_to_keep += list(range(start,r[0]+1))
        start = r[1]

    indices_to_keep += list(range(start, len(x)))

    new_x = []
    new_y = []
    for i in indices_to_keep:
        new_x.append(x[i])
        new_y.append(y[i])

    # TODO: output the same type as input?
    return new_x, new_y

def array_contains_n_consecutive_vals(arr, val, n):
    """
    Given a 1-d array, a value, and n, check if the array contains
    n consecutive elements that have that value.
    """
    if not is_one_d_array(arr):
        print("ERROR: input must be 1-d array")
        raise TypeError
    if not isinstance(val, type(arr[0])):
        print(f"ERROR: the input value type ({type(val)}) is not consistent with that of array elements ({type(arr[0])}).")
        raise TypeError
    if not isinstance(n, (int, np.int_)):
        print("ERROR: n must be an integer.")
        raise TypeError

    if n <= 0:
        print("ERROR: n must be bigger than 0.")
        raise ValueError

    if n > len(arr):
        return False

    ptrs = [i for i in range(n)]
    while ptrs[-1] < len(arr):
        if all([arr[i] == val for i in ptrs]):
            return True
        ptrs = [p+1 for p in ptrs]

    return False

def get_number_of_zeros_after_decimal(number):
    """
    Given a float < 1, find number of zeros after decimal point.
    """
    if not isinstance(number, (float, np.float_)):
        print("ERROR: number should be a float.")
        raise TypeError

    if np.abs(number) >= 1:
        print(f"ERROR: |{number}| is >= 1.")
        raise ValueError

    # TODO: float vs. higher precision?
    num_str = f"{number:.16f}".split('.')[1]
    ct = 0
    for char in num_str:
        if char != '0':
            break
        ct += 1

    return ct

def is_num_in_range(num, range_1):
    """
    Given a number and a range, check if number in range.

    If range = (a, b), returns true if num in [a,b].
    """
    if num >= range_1[0] and num <= range_1[1]:
        return True
    return False

def find_intersection_of_two_lines(pts1=None, pts2=None, m=None, c=None):
    """
    Given two lines (as two sets of two points, or a set of slopes and y-ints),
    find the point of intersection.
    """
    if pts1 is None:
        if m is None or c is None:
            print("ERROR: insufficient information.")
            raise ValueError
        elif len(m) == 2 and len(c) == 2:
            m1 = m[0]
            m2 = m[1]
            c1 = c[0]
            c2 = c[1]
        else:
            raise ValueError
    else:
        if pts2 is None:
            raise ValueError
        if m is not None or c is not None:
            print("WARNING: you provided both points and slopes/intercepts. Using the points only.")

        #TODO: check length/type of pts1 and pts2
        m1 = (pts1[0][1] - pts1[0][1]) / (pts1[0][0] - pts1[0][0])
        m2 = (pts2[0][1] - pts2[0][1]) / (pts2[0][0] - pts2[0][0])
        c1 = pts1[0][1] - m1 * pts1[0][0]
        c2 = pts2[0][1] - m2 * pts2[0][0]

    x = (c1 - c2) / (m2 - m1)
    y = m1 * x + c1
    
    return x, y

def linear_interp(x1, x2, y1, y2, x_query):
    """
    Consider a line segmend (x1, y1) -> (x2, y2). Given
    x_query in (x1, x2), find y_query, using linear interpolation.
    """
    if not is_num_in_range(x_query):
        print(f"WARNING: {x_query} not in ({x1}, {x2}).")
        return None

    # vertical line
    # TODO: redundant?
    if x1 == x2 and x1 != x_query:
        print(f"WARNING: {x_query} not in ({x1}, {x2}).")
        return None

    if x_query == x1:
        return y1
    if x_query == x2:
        return y2

    # horizontal line
    if y1 == y2:
        return y1

    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1

    return slope * x_query + intercept

def expand_data_with_linear_interp(x, y, x_query):
    """
    Given a curve defined by x & y, and given x_query values,
    get y_query by linear interpolation.

    Assuming x is sorted.
    """
    x = np.array(x)
    y = np.array(y)
    y_query = []
    for val in x_query:
        diff = x - val
        idx = np.argpartition(diff, 2)
        y_val = linear_interp(x[idx[0]], x[idx[1]], y[idx[0]], y[idx[1]], val)
        y_query.append(y_val)

    return y_query

def sort_arrays(ref_array, to_be_sorted):
    """
    Function to sort arrays in a list, given a reference array.
    """
    if not is_one_d_num_array(ref_array):
        print("ERROR: ref array must be a 1d num array.")
        raise TypeError

    if not isinstance(to_be_sorted, list):
        print("ERROR: to_be_sorted must be a list")
        raise TypeError

    if is_one_d_array(to_be_sorted):
        to_be_sorted = [to_be_sorted]
    else:
        if not all([is_one_d_array(el) for el in to_be_sorted]):
            raise TypeError

    indices = np.argsort(np.array(ref_array))
    result = [[ref_array[i] for i in indices]]
    for arr in to_be_sorted:
        new_arr = [arr[i] for i in indices]
        result.append(new_arr)

    return result