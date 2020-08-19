
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

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(10,10), index=50)

    # Prescribed masking parameters
    # 1 Sigma
    sigma_multiple = 1
    sigma_iterations = 2
    # Create the mask.
    test_mask = mono.mask.mask_sigma_value(
        data_array=test_array, sigma_multiple=sigma_multiple, 
        sigma_iterations=sigma_iterations)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '92.7429789714003440708375243748487223136051046'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    product = mono.math.integer_array_product(
        array=test_masked_array.compressed())
    product_log10 = sy.Float(sy.N(sy.log(sy.Integer(product), 10)))

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_percent_truncation():
    """ This tests the masking of percent truncations."""

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(7,7))

    # Prescribed masking parameters
    # The top 35% and bottom 10%.
    top_percent = 0.35
    bottom_percent = 0.10
    # Create the mask.
    test_mask = mask.mask_percent_truncation(
        data_array=test_array, top_percent=top_percent, 
        bottom_percent=bottom_percent)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '48.3986809684295405908025212823332315778806862'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = mono.math.integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_pixel_truncation():
    """ This tests the masking of pixel boundaries."""

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(7,7))

    # Prescribed masking parameters
    # Top 13 pixels and bottom 9.
    top_count = 13
    bottom_count = 9
    # Create the mask.
    test_mask = mask.mask_pixel_truncation(data_array=test_array,
                                               top_count=top_count,
                                               bottom_count=bottom_count)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '51.0043131557317283360473320982116998982267737'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = mono.math.integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_maximum_value():
    """ This tests the masking of values above a maximum."""

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(7,7))

    # Prescribed masking parameters
    # The value 113 should not be masked.
    maximum_value = 113
    # Create the mask.
    test_mask = mask.mask_maximum_value(data_array=test_array,
                                            maximum_value=maximum_value)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '46.4998252465517387337527237516559582272076600'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = mono.math.integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_minimum_value():
    """ This tests the masking of values below a minimum."""

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(7,7))

    # Prescribed masking parameters.
    # The value 101 itself should not be masked.
    minimum_value = 101
    # Create the mask.
    test_mask = mask.mask_minimum_value(data_array=test_array,
                                            minimum_value=minimum_value)
    # Create a mask array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '52.5579255086291590806495158287835916351211866'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = mono.math.integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_exact_value():
    """ This tests the masking of exact values."""

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(7,7))

    # Prescribed masking parameters
    exact_value = 101
    # Create the mask.
    test_mask = mask.mask_exact_value(data_array=test_array,
                                          exact_value=exact_value)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '86.9163820638011874618505104537286754939523446'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = mono.math.integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_invalid_value():
    """ This tests the masking of invalid values."""

    # Creating the testing array.
    test_array = mono._test.create_prime_test_array(shape=(7,7))

    # We need to force invalid values as the prime test creation
    # does not have them.
    test_array = np.array(test_array,dtype=float)
    test_array[1:3,2] = np.inf
    test_array[2,4:6] = -np.inf
    test_array[5,1:6] = np.nan

    # Prescribed masking parameters
    pass
    # Create the mask.
    test_mask = mask.mask_invalid_value(data_array=test_array)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask)
    print(test_masked_array)
    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '70.8884174145533646297736729939104459590381610'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = mono.math.integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None
