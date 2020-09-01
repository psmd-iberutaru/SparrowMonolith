
"""
This section is dedicated to the testing of all invalid based 
masks.
"""

import random
import numpy as np
import pytest

import sparrowmonolith as mono

def test_mask_invalid_all():
    """ This tests the masking of infinities, both plus and minus,
    within an array.
    """
    def static_distribution():
        # The dummy array.
        dummy_array = np.array(
            [[2, np.nan, 3, 5, 7, np.nan, 2],
            [np.nan, 1, 3, 8, 2, 2, 4],
            [7, 2, -np.inf, 5, np.nan, 6, 9],
            [3, 3, 2, 1, np.inf, 6, 6],
            [np.inf, 5, 8, np.inf, 2, 6, 3],
            [8, 2, 4, 5, 4, np.inf, 5],
            [7, 9, -np.inf, 4, 8, 9, -np.inf]])
        # Expected mask.
        expected_mask = np.array(
            [[False, True, False, False, False, True, False],
            [True, False, False, False, False, False, False],
            [False, False, True, False, True, False, False],
            [False, False, False, False, True, False, False],
            [True, False, False, True, False, False, False],
            [False, False, False, False, False, True, False],
            [False, False, True, False, False, False, True]])
        # Test mask
        test_mask = mono.mask.mask_invalid_all(data_array=dummy_array)
        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do not "
                          "agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
        return None

        return None
    def random_distribution():
        # Invalid types.
        invalid_types = [np.nan, -np.inf, np.inf]

        # The dummy array made up of an invalid types, each test
        # will always use a different random type.
        rand_array = np.random.random([7,7])
        dummy_array = np.where(rand_array <= 0.25, 
                               random.choice(invalid_types), rand_array)

        # The expected mask, as these are where the invalid types 
        # were put.
        expected_mask = np.where(rand_array <= 0.25, True, False)

        # Test the masking of invalid all.
        test_mask = mono.mask.mask_invalid_all(data_array=dummy_array)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do not "
                          "agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message
        return None

    # Run the masks.
    static_distribution()
    random_distribution()
    # All done.
    return None


def test_mask_invalid_infinity():
    """ This tests the masking of infinities, both plus and minus,
    within an array.
    """
    # Dummy data array to use.
    dummy_array = [[0, -np.inf, 0, 0, 0, -np.inf],
                   [0, np.inf, 0, 0, 0, 0],
                   [0, 0, -np.inf, 0, 0, 0],
                   [0, 0, 0, 0, np.inf, 0],
                   [np.inf, 0, 0, 0, 0, 0],
                   [0, 0, 0, np.inf, 0, 0]]
    dummy_array = np.array(dummy_array, dtype=float)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 1, 0, 0, 0, 1],
                     [0, 1, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    pass

    # Making the test mask.
    test_mask = mono.mask.mask_invalid_infinity(data_array=dummy_array)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_invalid_positive_infinity():
    """ This tests the masking of infinities, only plus,
    within an array.
    """
    # Dummy data array to use.
    dummy_array = [[0, -np.inf, 0, 0, 0, -np.inf],
                   [0, np.inf, 0, 0, np.inf, 0],
                   [0, 0, -np.inf, 0, 0, 0],
                   [0, 0, 0, 0, np.inf, 0],
                   [np.inf, 0, 0, 0, 0, 0],
                   [0, 0, 0, np.inf, 0, -np.inf]]
    dummy_array = np.array(dummy_array, dtype=float)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0],
                     [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    pass

    # Making the test mask.
    test_mask = mono.mask.mask_invalid_positive_infinity(
        data_array=dummy_array)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_invalid_negetive_infinity():
    """ This tests the masking of infinities, only minus,
    within an array.
    """
    # Dummy data array to use.
    dummy_array = [[0, -np.inf, 0, np.inf, 0, -np.inf],
                   [0, np.inf, 0, 0, np.inf, 0],
                   [0, 0, -np.inf, 0, 0, 0],
                   [0, 0, 0, 0, np.inf, 0],
                   [np.inf, 0, 0, 0, 0, 0],
                   [0, 0, -np.inf, np.inf, 0, -np.inf]]
    dummy_array = np.array(dummy_array, dtype=float)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 1, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 1]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    pass

    # Making the test mask.
    test_mask = mono.mask.mask_invalid_negetive_infinity(
        data_array=dummy_array)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None


def test_mask_invalid_nan():
    """ This tests the masking of NaN values within an array.
    """
    # Dummy data array to use.
    dummy_array = [[0, 0, 0, 0, 0, 0],
                   [0, np.nan, 0, 0, 0, 0],
                   [0, 0, 0, 0, np.nan, 0],
                   [0, 0, np.nan, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0],
                   [np.nan, 0, 0, np.nan, 0, 0]]
    dummy_array = np.array(dummy_array, dtype=float)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 1, 0, 0]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    pass

    # Making the test mask.
    test_mask = mono.mask.mask_invalid_nan(data_array=dummy_array)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None