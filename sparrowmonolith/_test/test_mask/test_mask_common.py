

"""
This section is dedicated to functions that are common across all
masking routines.
"""

import numpy as np

import sparrowmonolith as mono


def test_combine_masks_lor():
    """ This tests the synthesis of multiple masks into one mask.
    This only tests the combination of masks as a logical or.
    """

    def static():
        # Two dummy masks must be made to test the combination of
        # masks.
        dummy_mask_1 = np.array([0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 
                                 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 
                                 1, 0, 1, 1, 0], dtype=bool)
        dummy_mask_2 = np.array([0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 
                                 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 
                                 0, 0, 1, 0, 0], dtype=bool)
        # And the expected combined mask.
        expected_mask = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 
                                  1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 
                                  1, 0, 1, 1, 0], dtype=bool)

        # Create the test mask.
        test_mask = mono.mask.combine_masks_lor(dummy_mask_1, dummy_mask_2)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do not "
                          "agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message

    # Begin the tests.
    static()

    return None


def test_combine_masks_land():
    """ This tests the synthesis of multiple masks into one mask.
    This only tests the combination of masks as a logical and.
    """

    def static():
        # Two dummy masks must be made to test the combination of
        # masks.
        dummy_mask_1 = np.array([0, 0, 0, 1, 1, 0, 0, 1, 1, 1,
                                 0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
                                 1, 0, 0, 1, 0], dtype=bool)
        dummy_mask_2 = np.array([1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 
                                 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 
                                 1, 0, 0, 0, 0], dtype=bool)
        # And the expected combined mask.
        expected_mask = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 
                                  0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 
                                  1, 0, 0, 0, 0], dtype=bool)

        # Create the test mask.
        test_mask = mono.mask.combine_masks_land(dummy_mask_1, dummy_mask_2)

        # Check that they are the same.
        assert_message = ("The expected mask and the created mask do not "
                          "agree. "
                          "\n Test: \n {t_mask} \n Expected: \n {e_mask}"
                          .format(t_mask=test_mask, e_mask=expected_mask))
        assert np.array_equal(test_mask, expected_mask), assert_message

    # Begin the tests.
    static()

    return None