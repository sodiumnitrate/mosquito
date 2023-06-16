from mosquito.type_check import *

import pdb

class TestTypeCheck:
    def test_is_non_scalar(self):
        assert not is_non_scalar(5)
        assert is_non_scalar([5,10,11])
        assert is_non_scalar((5,55,555))
        assert is_non_scalar(np.array([5,5,5]))
        assert is_non_scalar([])

    def test_is_one_d_array(self):
        assert not is_one_d_array(5)
        assert is_one_d_array([5,55])
        assert not is_one_d_array([5,[55]])
        assert is_one_d_array(np.array([5,55]))
        assert not is_one_d_array(np.array([[55,5],[22,2]]))
        assert is_one_d_array((5,55,55))
        assert not is_one_d_array(((5,55),5))

        assert is_one_d_array([])


    def test_is_one_d_int_array(self):
        assert is_one_d_int_array([5,10])
        assert not is_one_d_int_array([5.5, 10])

        assert is_one_d_int_array([])