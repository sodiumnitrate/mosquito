"""
This script contains multiple tools to check types of input
variables that are non-standard but that I encounter commonly.
"""
import numpy as np

def is_non_scalar(arr):
    """
    Checks if input is a list, or np array, or tuple.
    """
    return isinstance(arr, (list, tuple, np.ndarray))

def is_one_d_array(arr):
    """
    Checks if input is a 1d list or 1d np.ndarray or 1d tuple.

    Empty array passes the check.
    """
    if not is_non_scalar(arr):
        return False

    if any([is_non_scalar(a) for a in arr]):
        return False

    return True

def is_one_d_int_array(arr):
    """
    Checks if input is a 1d array of integers.

    Empty array passes the check.
    """
    if not is_one_d_array(arr):
        return False

    if not all([isinstance(a, (int, np.int_)) for a in arr]):
        return False

    return True