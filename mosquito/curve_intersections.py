"""
Contains a class that takes input about two sets of data, and can
determine intersections between them.
"""

import numpy as np

from mosquito.type_check import is_one_d_array, is_non_scalar, is_one_d_num_array
from mosquito.mosquito import sort_arrays, find_intersection_of_two_lines

class CurveIntersections:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.shared_x = None
        self.check_data()

        self.tangent = None
        self.n_points = None
        self.int_x = None
        self.int_y = None
        self.diff = None
        self.int_idx = None

    def check_data(self):
        """
        Check the input data for validity, and determine whether the curves
        share x-values.
        """
        if not is_non_scalar(self.y):
            raise TypeError
        else:
            if len(self.y) != 2:
                raise ValueError
            if not is_one_d_num_array(self.y[0]) or not is_one_d_num_array(self.y[1]):
                raise TypeError

        if is_one_d_num_array(self.x):
            self.shared_x = True
        elif not is_one_d_array(self.x):
            if len(self.x) != 2:
                raise ValueError
            if not is_one_d_num_array(self.x[0]) or not is_one_d_num_array(self.x[1]):
                raise TypeError
            if self.x[0] == self.x[1]:
                self.shared_x = True
                self.x = self.x[0]
            else:
                self.shared_x = False
        else:
            raise TypeError

        # sort data such that x is monotonically increasing
        if self.shared_x:
            sorted_data = sort_arrays(self.x, self.y)
            self.x = sorted_data[0]
            self.y = [sorted_data[1], sorted_data[2]]
        else:
            sorted_data = sort_arrays(self.x[0], self.y[0])
            self.x[0] = sorted_data[0]
            self.y[0] = sorted_data[1]
            sorted_data = sort_arrays(self.x[1], self.y[1])
            self.x[1] = sorted_data[0]
            self.y[1] = sorted_data[1]

    def find_intersections(self, interpolate=False):
        """
        Given two curves, find their intersections.

        interpolate can be:
        - False (return closest x-value)
        - linear

        # TODO: implement spline interp
        """

        if self.shared_x:
            self.find_intersections_shared_x(interpolate=interpolate)


    def find_intersections_shared_x(self, interpolate=False):
        """
        Function to find intersections between the curves, given the x-values are
        shared.
        """
        x = np.array(self.x)
            
        y1 = np.array(self.y[0])
        y2 = np.array(self.y[1])

        # the difference between the two curves at all x
        diff = y1 - y2

        # zero out below tolerance
        diff[np.where(np.abs(diff) < 1e-15)] = 0

        self.diff = diff

        # determine the index and number of intersection points
        # if there are more than one consecutive intersection points, only the first
        # and the last are taken.
        int_idx = []
        n_points = 0
        prev_ptr = 0
        ptr = 1
        tangent = False
        while ptr < len(diff):
            prev_val = diff[prev_ptr]
            curr = diff[ptr]
            if curr == 0 and prev_val != 0:
                n_points += 1
                int_idx.append(curr)
                tangent = True
            elif curr != 0 and prev_val == 0:
                if not tangent:
                    n_points += 1
                    int_idx.append(ptr)
                    tangent = False
            elif curr == 0 and prev_val == 0:
                tangent = False
                self.tangent = True
            else:
                # none of them are zero
                if curr*prev_val < 0:
                    # sign change
                    n_points += 1
                    int_idx.append((prev_ptr,ptr))
            ptr += 1
            prev_ptr += 1

        self.n_points = n_points
        self.int_idx = int_idx

        # get indices, and x- and y-values of intersections
        self.int_idx = []
        x_int = []
        y_int = []
        for idx in int_idx:
            if isinstance(idx, (int, np.int_)):
                x_int.append(x[idx])
                y_int.append(y1[idx])
                self.int_idx.append(idx)
            else:
                # then we have a sign change
                a = idx[0]
                b = idx[1]
                if interpolate:
                    x, y = find_intersection_of_two_lines(pts1=[[x[a], x[b]], [y1[a], y1[b]]],
                                                          pts2=[[x[a], x[b]], [y2[a], y2[b]]])
                else:
                    if np.abs(diff[a]) < np.abs(diff[b]):
                        x_int.append(x[a])
                        y_int.append(y1[a])
                        self.int_idx.append(a)
                    else:
                        x_int.append(x[b])
                        y_int.append(y1[b])
                        self.int_idx.append(b)
        self.int_x = x_int
        self.int_y = y_int

    def get_spans_below_curve(self, reverse=False):
        """
        Get ranges of indices for which y1 < y2.
        """
        if self.int_idx is None:
            self.find_intersections()

        if len(self.int_idx) == 0:
            print("ERROR: no intersections found.")
            raise ValueError

        diff = self.diff
        if reverse:
            diff *= -1

        # get all spans
        spans = [(0,self.int_idx[0])]
        for i in range(len(self.int_idx)-1):
            spans.append((self.int_idx[i],self.int_idx[i+1]))
        spans.append((self.int_idx[-1], len(self.y[0])-1))

        final_spans = []
        for span in spans:
            if span[1]-span[0] > 1:
                idx = span[0] + 1
                if diff[idx] < 0:
                    final_spans.append(span)

        return final_spans
