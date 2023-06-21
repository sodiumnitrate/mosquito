"""
This file contains tools to print strings, especially with
color, using colorama.
"""

from mosquito.mosquito import check_overlap_range_list_of_lists, check_overlap_range_list, is_num_in_range
from colorama import Fore, Back, Style

different_colors = [Fore.RED, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.RED, Fore.YELLOW,
                    Fore.RED+Back.CYAN, Fore.BLUE+Back.WHITE, Fore.BLUE+Back.YELLOW, Fore.YELLOW+Back.BLUE,
                    Fore.WHITE+Back.RED, Fore.GREEN+Back.BLUE]

def color_char(char, color=Fore.BLUE):
    """
    Given a char and a color, return colored char.
    """
    res = f"{color}{char}{Style.RESET_ALL}"
    return res

def color_string_with_ranges(string, list_of_ranges, list_of_colors=None, allow_overlap=False):
    """
    Given a string, and a list of ranges, generate a string that colors
    each range differently. If a list of colors is also provided, then use
    that. If not, pick colors randomly.
    
    list_of_ranges can be one of the following:
    1- [(a,b), (c,d), ...]
    2- [[(a,b), (c,d)], [(e,f)], ...]
    3- (a,b)

    In (1), each range will be colored differently. In (2), all the ranges
    in a given sublist will be colored the same, but each sublist will have
    different colors.

    For (3), just color one span.
    """

    if not isinstance(string, str):
        print("ERROR: the string input is not of type string.")
        raise TypeError

    if isinstance(list_of_ranges, tuple):
        if len(list_of_ranges) != 2:
            print("ERROR: a range must have two elements.")
            raise TypeError

        list_of_ranges = [list_of_ranges]
        list_of_lists = False
        list_of_tuples = True
    elif isinstance(list_of_ranges, list):
        list_of_lists = all([isinstance(l, list) for l in list_of_ranges])
        list_of_tuples = all([isinstance(l, tuple) for l in list_of_ranges])
        if list_of_lists:
            for l in list_of_ranges:
                if not all([isinstance(el, tuple) for el in l]):
                    print("ERROR: not a list of tuples.")
                    raise TypeError
                elif not all([len(el)==2 for el in l]):
                    print("ERROR: tuples must have two elements.")
                    raise TypeError
        elif list_of_tuples:
            if not all([len(el)==2 for el in list_of_ranges]):
                print("ERROR: tuples must have two elements.")
                raise TypeError
        else:
            print(f"ERROR: {type(list_of_ranges[0])} not recognized.")
            raise TypeError
    else:
        print(f"ERROR: {type(list_of_ranges)} not recognized.")
        raise TypeError

    # figure out the color situation
    n_colors = len(list_of_ranges)
    if n_colors > len(different_colors):
        print("ERROR: too many colors requested.")
        raise ValueError

    if list_of_colors is None:
        list_of_colors = different_colors[:n_colors]
    else:
        # TODO: check for valid colors (how?)
        pass

    # check ranges for overlaps
    if n_colors != 1 and not allow_overlap:
        if list_of_lists:
            if check_overlap_range_list_of_lists(list_of_ranges):
                print("ERROR: overlap in ranges.")
                raise ValueError
        if list_of_tuples:
            if check_overlap_range_list(list_of_ranges):
                print("ERROR: overlap in ranges.")
                raise ValueError

    # create result string
    res = ""
    for i, char in enumerate(string):
        color = None
        for c_idx in range(n_colors):
            if list_of_lists:
                ranges = list_of_ranges[c_idx]
            else:
                ranges = [list_of_ranges[c_idx]]
            for r in ranges:
                if is_num_in_range(i, r):
                    color = list_of_colors[c_idx]
        if color:
            res += color_char(char, color=color)
        else:
            res += char

    return res