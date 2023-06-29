"""
This file contains various functions and tools for file IO.
"""

import numpy as np
import io
import os


def file_len(fname):
    """Function to get the number of lines in a file."""
    count = 0
    with open(fname, 'r') as f:
        for line in f:
            count += 1

    return count

def tail(f,n=10):
    """
    Function to get the last n lines of a file (efficiently).

    Returns a list of strings.
    """
    if not isinstance(f, io.IOBase):
        if isinstance(f, str):
            f = open(f,'r')
        else:
            raise TypeError

    if not isinstance(n, (int, np.int_)):
        raise TypeError

    if n <= 0:
        raise ValueError

    pos, lines = n+1, []

    # set file pointer to end
    f.seek(0, os.SEEK_END)

    is_file_small = False

    while len(lines) <= n:
        try:
            f.seek(f.tell() - pos, os.SEEK_SET)
        except ValueError as e:
            # lines greater than file seeking size
            # seek to start
            f.seek(0, os.SEEK_SET)
            is_file_small = True
        finally:
            lines = f.readlines()
            if is_file_small:
                break

        pos*= 2
    rel_lines = [l.strip() for l in lines[-n:]]
    return rel_lines


def check_if_end_of_file_contains(file_name,contained_string,n=10):
    """
    Checks if the given string exists somewhere within the last n lines of the file.
    """
    if not os.path.exists(file_name):
        return False
    f = open(file_name,'r')

    lines =tail(f,n=n)
    for line in lines:
        if contained_string in line:
            return True

    return False