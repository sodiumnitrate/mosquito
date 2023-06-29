"""
Unit tests for CurveIntersections.
"""

from mosquito.curve_intersections import CurveIntersections

import pdb

class TestCurveIntersections:
    def test_init(self):
        x = [1,2,3,4,5]
        y1 = [2,3,4,5,6]
        y2 = [1,2,5,6,7]

        ci = CurveIntersections(x, [y1, y2])

        assert ci.shared_x

        x = [[1,2,3,4,5],[2,3,4,5,6]]
        ci = CurveIntersections(x, [y1, y2])

        assert not ci.shared_x

    def test_find_intersections(self):
        x = [1,2,3,4,5]
        y1 = [2,3,4,5,6]
        y2 = [1,2,5,6,7]

        ci = CurveIntersections(x, [y1, y2])

        ci.find_intersections()

        assert ci.n_points == 1
        assert not ci.tangent 

        assert ci.int_x is not None
        assert ci.int_y is not None
        assert ci.diff is not None

    def test_find_intersections_2(self):
        x = [1,2,3,4,5]
        y1 = [2,3,4,5,6]
        y2 = [1,2,4,5,7]

        ci = CurveIntersections(x, [y1, y2])

        ci.find_intersections()

        assert ci.n_points == 2
        assert ci.tangent

    def test_find_intersections_3(self):
        x = [1,2,3,4,5]
        y1 = [2,3,4,5,6]
        y2 = [1,2,4,6,7]

        ci = CurveIntersections(x, [y1, y2])

        ci.find_intersections()

        assert ci.n_points == 1
        assert not ci.tangent

    def test_spans_below_curve(self):
        x = [0,1,2,3,4,5,6]
        y1 = [1,2,3,4,5,6,7]
        y2 = [0,1,2,5,6,7,8]

        ci = CurveIntersections(x, [y1, y2])

        ci.find_intersections()
        test = ci.get_spans_below_curve()

        assert test[0][0] == 3
        assert test[0][1] == 6

        