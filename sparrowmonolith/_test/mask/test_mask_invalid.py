
"""
This section is dedicated to the testing of all invalid based 
masks.
"""

import numpy as np

import sparrowmonolith as mono

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