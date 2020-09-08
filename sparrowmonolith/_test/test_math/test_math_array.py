
"""
This section is dedicated to the testing of all array based 
calculations.
"""

import sympy as sy
import math
import pytest

import sparrowmonolith as mono

@pytest.mark.skip(reason="Not implemented.")
def test_integer_array_sum():
    """ This tests the summation of large integers in an array.
    """
    assert False
    return None

@pytest.mark.skip(reason="Not implemented.")
def test_float_array_sum():
    """ This tests the summation of large floats in an array.
    """
    assert False
    return None

def test_integer_array_product():
    """ This tests the multiplication of large integers in an array. 
    """

    # Creating the testing array of integers.
    test_array = mono._test.create_prime_test_array(shape=(5,5),index=13)

    # The products of the multiplication.
    product = mono.math.array.integer_array_product(array=test_array)
    product_nat_log = sy.Float(sy.N(sy.log(product)))
    product_log10 = sy.Float(sy.N(sy.log(product, 10)))
    
    # Checking the values against results from Wolfram|Alpha. 
    # Sparrow thinks Wolfram|Alpha is a "correct" enough source.
    # See https://cutt.ly/ZuccSbe for Wolfram|Alpha computation.
    CHECK_PROD_STRING = '18952004028289913475831259188568511277704891202961'
    CHECK_NUMBER = sy.Integer(CHECK_PROD_STRING)
    # See https://cutt.ly/quccGdx for Wolfram|Alpha computation.
    CHECK_NLOG_STRING = '113.4659941431228872468758215004232622784893568421'
    CHECK_NLOG = sy.Float(CHECK_NLOG_STRING)
    # See https://cutt.ly/fuccHAI for Wolfram|Alpha computation.
    CHECK_B10_STRING = '49.277655140024960622131491261439997397213580891331'
    CHECK_B10LOG = sy.Float(CHECK_B10_STRING)

    # Checking the product itself.
    prod_assert_message = ("The check number is: {check}  "
                           "The product is: {prod} "
                           .format(check=CHECK_NUMBER, prod=product))
    assert math.isclose(product, CHECK_NUMBER), prod_assert_message

    # Checking the natural log of the product.
    nlog_assert_message = ("The check logarithm is: {check}  "
                           "The product natural logarithm is: {log} "
                           .format(check=CHECK_NLOG, log=product_nat_log))
    assert math.isclose(product_nat_log, CHECK_NLOG), nlog_assert_message

    # Checking the base 10 log itself.
    b10log_assert_message = ("The check logarithm is: {check}  "
                             "The product base 10 logarithm is: {log} "
                             .format(check=CHECK_B10LOG, log=product_log10))
    assert math.isclose(product_log10, CHECK_B10LOG), b10log_assert_message
    # All done.
    return None

@pytest.mark.skip(reason="Not implemented.")
def test_float_array_product():
    """ This tests the multiplication of large floats in an array.
    """
    assert False
    return None