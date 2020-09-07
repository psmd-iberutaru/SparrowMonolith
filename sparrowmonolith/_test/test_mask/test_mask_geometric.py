
"""
This section is dedicated to the testing of all geometric based 
masks.
"""


import numpy as np

import sparrowmonolith as mono

def test_mask_single_pixels():
    """ This tests the masking of single pixels in a single array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 0, 0, 0, 0, 1],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 1],
                     [0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 1]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    column_indexes = [1,2,3,5,5,5]
    row_indexes = [3,1,4,0,3,5]

    # Making the test mask.
    test_mask = mono.mask.mask_single_pixels(
        data_array=dummy_array, column_indexes=column_indexes, 
        row_indexes=row_indexes)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_rectangle():
    """ This tests the masking of a rectangle in an array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0, 0]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    column_range = [2,4]
    row_range = [1,4]

    # Making the test mask.
    test_mask = mono.mask.mask_rectangle(
        data_array=dummy_array, column_range=column_range, 
        row_range=row_range)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_subarray():
    """ This tests the masking of all but a single sub-array in an
    array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 1, 1],
                     [0, 0, 0, 0, 1, 1],
                     [0, 0, 0, 0, 1, 1],
                     [0, 0, 0, 0, 1, 1],
                     [1, 1, 1, 1, 1, 1]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    column_range = [0,3]
    row_range = [1,4]

    # Making the test mask.
    test_mask = mono.mask.mask_subarray(
        data_array=dummy_array, column_range=column_range, 
        row_range=row_range)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_columns():
    """ This tests the masking of columns in an array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 1, 0, 0, 1, 1],
                     [0, 1, 0, 0, 1, 1],
                     [0, 1, 0, 0, 1, 1],
                     [0, 1, 0, 0, 1, 1],
                     [0, 1, 0, 0, 1, 1],
                     [0, 1, 0, 0, 1, 1]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    column_list = [1,4,5]

    # Making the test mask.
    test_mask = mono.mask.mask_columns(
        data_array=dummy_array, column_list=column_list)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_rows():
    """ This tests the masking of rows in an array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    row_list = [1,2,4,5]

    # Making the test mask.
    test_mask = mono.mask.mask_rows(data_array=dummy_array, row_list=row_list)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_nothing():
    """ This tests the masking of nothing in an array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    pass

    # Making the test mask.
    test_mask = mono.mask.mask_nothing(data_array=dummy_array)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None

def test_mask_everything():
    """ This tests the masking of everything in an array.
    """
    # Dummy data array to use.
    dummy_array = np.random.rand(6,6)
    # The masking that should be produced by the masking function.
    expected_mask = [[1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1]]
    expected_mask = np.array(expected_mask, dtype=bool)
    # The two arrays should have the same shape.
    assert dummy_array.shape == expected_mask.shape, "Invalid test array."

    # The parameters for the testing pixels to replicate above.
    pass

    # Making the test mask.
    test_mask = mono.mask.mask_everything(data_array=dummy_array)

    # Check that they are the same.
    assert_message = ("The expected mask and the created mask do not agree. "
                      "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                      .format(t_mask=test_mask, e_mask=expected_mask))
    assert np.array_equal(test_mask, expected_mask), assert_message
    # All done.
    return None












