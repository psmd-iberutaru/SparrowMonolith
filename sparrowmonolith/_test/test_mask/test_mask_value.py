
"""
This section tests the masks that are based on the values of the
entries within an array.
"""

import numpy as np
import numpy.ma as np_ma
import sympy as sy
import math

import sparrowmonolith as mono


def test_mask_sigma_value():
    """ This tests the masking of sigma boundaries."""

    def static():
        # A static test using known values.
        # The dummpy array for testing.
        dummy_array = np.array(
            [68.62085908, 62.94584769, 46.10159024, 2.32740926, 68.55825449, 
             97.99261137, 18.82252072, 17.77134184, 99.8657068, 74.19160885, 
             10.81813721, 30.56502282, 47.07526169, 49.3529831, 8.149068235, 
             17.24015438, 33.67543865, 81.97499641, 15.4345859, 86.07152409, 
             73.92317237, 74.18056898, 17.91157475, 64.7076976, 33.84952066, 
             44.44174694, 32.28096427, 61.19345933, 2.26349089, 67.72506891, 
             29.81437395, 78.07069183, 39.72793038, 78.4748242, 64.71906276])
        # The mean and std.
        mean = mono.math.statistics.arithmetic_mean(array=dummy_array)
        std = mono.math.statistics.standard_deviation(array=dummy_array)
        sigma = 1
        # The expected mask.
        expected_mask = np.array([False, False, False, True, False, 
                                  True, True, True, True, False, 
                                  True, False, False, False, True, 
                                  True, False, True, True, True, 
                                  False, False, True, False, False, 
                                  False, False, False, True, False, 
                                  False,  True, False, True, False])
        # Compute the mask.
        test_mask = mono.mask.mask_sigma_value(data_array=dummy_array, 
                                               sigma_multiple=sigma, 
                                               sigma_iterations=1)
        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
        return None
    def dynamic():
        # A test using random values with the simple principle.
        # The dummpy array for testing.
        dummy_array = (np.random.random(np.random.randint(100))
                      * np.random.randint(1000))
        # The mean and std. (This also somewhat tests the mean and
        # std functions.)
        mean = mono.math.statistics.arithmetic_mean(array=dummy_array)
        std = mono.math.statistics.standard_deviation(array=dummy_array)
        sigma = 1
        # The expected mask.
        expected_mask = np.where(
            np.logical_and((mean - sigma*std <= dummy_array),
                           (dummy_array <= mean + sigma*std)), False, True)
        # Compute the mask.
        test_mask = mono.mask.mask_sigma_value(data_array=dummy_array, 
                                               sigma_multiple=sigma, 
                                               sigma_iterations=1)
        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
        return None


    # Do the tests.
    static()
    dynamic()

    # All done.
    return None

def test_mask_percent_truncation():
    """ This tests the masking of percent truncations."""
    def similar():
        # The discrete values to be masked.
        dummy_array = np.array([2, 5, 3, 8, 9, 7, 3, 7, 0, 7, 
                                1, 8, 2, 1, 1, 8, 4, 9, 2, 4])
        # Masking the top 15% and bottom 25% values.
        expected_mask = np.array([False, False, False, False, True, 
                                  False, False, False, True, False, 
                                  True, False, False, True, True, 
                                  False, False, True, False, False])
        # And the test mask. Masking the top 15% and bottom 
        # 25% values.
        test_mask = mono.mask.mask_percent_truncation(
            data_array=dummy_array, top_percent=0.15, bottom_percent=0.25)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
    def unsimilar():
    # The discrete values to be masked.
        dummy_array = np.array([75, 15, 59, 73, 16, 54, 28, 90, 50, 61, 
                                46, 25, 48, 94, 44,  9, 29, 47, 30, 76])
        # Masking the top 10% and bottom 15% values.
        expected_mask = np.array([False, True, False, False, True, 
                                  False, False, True, False, False, 
                                  False, False, False, True, False, 
                                  True, False, False, False, False])
        # And the test mask. Masking the top 10% and bottom 
        # 15% values.
        test_mask = mono.mask.mask_percent_truncation(
            data_array=dummy_array, top_percent=0.10, bottom_percent=0.15)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
    # Do the mask tests.
    similar()
    unsimilar()
    # All done.
    return None

def test_mask_count_truncation():
    """ This tests the masking of discrete values truncations."""

    def similar():
        # The discrete values to be masked.
        dummy_array = np.array([4, 5, 5, 9, 6, 7, 7, 3, 0, 1, 
                                7, 5, 7, 5, 1, 3, 8, 4, 6, 8])
        # Masking the top 4 and bottom 5 values.
        expected_mask = np.array([False, False, False, True, False, 
                                  False, False, False, True, True, 
                                  False, False, False, False, True, 
                                  False, True, False, False, True])
        # And the test mask. Masking the top 5 and bottom 4 values.
        test_mask = mono.mask.mask_count_truncation(
            data_array=dummy_array, top_count=5, bottom_count=4)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
    def unsimilar():
    # The discrete values to be masked.
        dummy_array = np.array([45, 31, 18, 35, 23, 49, 33, 39,  3, 20, 
                                38, 44, 13, 24, 14, 37, 30, 32, 27, 19])
        # Masking the top 4 and bottom 7 values.
        expected_mask = np.array([True, False, True, False, True, 
                                  True, False, True, True, True, 
                                  False, True, True, False, True, 
                                  False, False, False, False, True])
        # And the test mask. Masking the top 4 and bottom 7 values.
        test_mask = mono.mask.mask_count_truncation(
            data_array=dummy_array, top_count=4, bottom_count=7)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
    # Do the mask tests.
    similar()
    unsimilar()
    # All done.
    return None

def test_mask_maximum_value():
    """ This tests the masking of values below a minimum."""
    # Dummy array
    dummy_array = np.array([3.60521638, 0.7734354 , 1.09878221, 
                            8.88359187, 9.18262154, 2.83727912, 
                            5.47739306, 4.1412989 , 6.15100436, 
                            2.01962448, 9.31029359, 6.69720493, 
                            0.31968758, 9.87020051, 8.67635648])
    # Maximum value
    upper_bound = 7.0
    expected_mask = np.array([False, False, False, 
                              True, True, False, 
                              False, False, False, 
                              False, True, False, 
                              False, True, True])
    # And the test mask.
    test_mask = mono.mask.mask_maximum_value(data_array=dummy_array, 
                                             maximum_value=upper_bound)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do "
                      "not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    return None

def test_mask_minimum_value():
    """ This tests the masking of values below a minimum."""
    # Dummy array
    dummy_array = np.array([8.92319810, 7.76177463, 5.24338828, 
                            5.16445421, 3.46879229, 7.90418040, 
                            9.89971106, 0.35017451, 7.03217028, 
                            7.76177463, 9.94345452, 7.76177463, 
                            1.01315397, 6.27653524, 2.23698335])
    # Minimum value
    lower_bound = 5.0
    expected_mask = np.array([False, False, False, 
                              False, True, False, 
                              False, True, False, 
                              False, False, False, 
                              True, False, True])
    # And the test mask.
    test_mask = mono.mask.mask_minimum_value(data_array=dummy_array, 
                                             minimum_value=lower_bound)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do "
                      "not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    return None

def test_mask_exact_value():
    """ This tests the masking of exact values."""

    def integers():
        # Dummy array
        dummy_array = np.array([7, 9, 5, 3, 9, 1, 7, 3, 1, 4, 3, 2, 7])
        # Same number = 7
        exact = 7
        expected_mask = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
                                 dtype=bool)
        # And the test mask.
        test_mask = mono.mask.mask_exact_value(
            data_array=dummy_array, exact_value=exact)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
        return None
    def floats():
        # Dummy array
        dummy_array = np.array([8.92319810, 7.76177463, 5.24338828, 
                                5.16445421, 8.46879229, 7.90418040, 
                                9.89971106, 0.35017451, 7.03217028, 
                                7.76177463, 9.94345452, 7.76177463, 
                                1.01315397, 6.27653524, 2.23698335])
        # Same number = 7
        exact = 7.76177463
        expected_mask = np.array([False, True, False, 
                                  False, False,False, 
                                  False, False, False, 
                                  True, False, True, 
                                  False, False, False])
        # And the test mask.
        test_mask = mono.mask.mask_exact_value(
            data_array=dummy_array, exact_value=exact)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do "
                          "not agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
        return None

    # Run the tests.
    integers()
    floats()
    # All done.
    return None
