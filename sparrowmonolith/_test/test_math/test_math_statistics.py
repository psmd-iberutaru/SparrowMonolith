

"""
This module is made for the complete computation of statistical
results.
"""

import decimal
import numpy as np
import math

import sparrowmonolith as mono

# Means and averages
##########

def test_arithmetic_mean():
    """ This tests the calculation of arithmetic means.
    """

    def example_calculation():
        # The array to use to test the calculation.
        test_array = [98, 59, 82, 75, 49, 91, 55, 77, 68, 
                      4, 42, 44, 50, 69, 1, 56, 76, 76, 37]
        # The expected mean result: 1109 / 19
        expected_mean = decimal.Decimal('58.368421052631578947368421052631579')
        # The calculated mean.
        calculated_mean = mono.math.statistics.arithmetic_mean(
            array=test_array)

        # Check.
        assert_message = ('Expected an arithmetic mean of `{expt}`, '
                          'calculated is `{calc}`. Array is: {arry}'
                          .format(expt=expected_mean, calc=calculated_mean,
                                  arry=test_array))
        assert math.isclose(expected_mean, calculated_mean), assert_message

    # Execute the tests.
    example_calculation()
# Aliases
def test_mean(): return test_arithmetic_mean()


def test_median():
    """ This tests the calculation of median. This tests both
    even and odd length arrays.
    """

    def example_odd_calculation():
        # The array to use to test the calculation.
        test_array = [98, 59, 82, 75, 49, 91, 55, 77, 68, 
                      4, 42, 44, 50, 69, 1, 56, 76, 76, 37]
        # The expected median result: 59
        expected_median = 59
        # The calculated mean.
        calculated_median = mono.math.statistics.median(array=test_array)

        # Check.
        assert_message = ('Expected a median of `{expt}`, '
                          'calculated is `{calc}`. Array is: {arry}'
                          .format(expt=expected_median, 
                                  calc=calculated_median,
                                  arry=test_array))
        assert expected_median == calculated_median, assert_message
    def example_even_calculation():
        # The array to use to test the calculation.
        test_array = [56, 10, 14, 60, 17, 33, 90, 79, 55, 9, 
                      72, 5, 81, 21, 99, 39, 73, 28, 18, 12]
        # The expected median result: 59
        expected_median = 36
        # The calculated mean.
        calculated_median = mono.math.statistics.median(array=test_array)

        # Check.
        assert_message = ('Expected a median of `{expt}`, '
                          'calculated is `{calc}`. Array is: {arry}'
                          .format(expt=expected_median, 
                                  calc=calculated_median,
                                  arry=test_array))
        assert expected_median == calculated_median, assert_message

    # Execute the tests.
    example_odd_calculation()
    example_even_calculation()

    # All done.
    return None

# Standard deviation
def test_standard_deviation():
    """ This tests the calculation of standard deviations. The 
    values of ddof=0 and ddof=1 are tested."""

    def population_ddof_0():
        # The test array.
        test_array = np.array([14, 17, 92, 57, 2, 92, 82, 2, 42, 64, 
                               94, 6, 87, 31, 67, 4, 68, 86, 14, 22])
        # The expected value: sqrt(467971) / 20
        expected_std = decimal.Decimal('34.20420295811612681408979427099')
        # Calculating.
        calculated_std = mono.math.statistics.standard_deviation(
            array=test_array, ddof=0)
        
        # Check.
        assert_message = ('Expected a standard deviation of `{expt}`, '
                          'calculated is `{calc}`. Array is: {arry}'
                          .format(expt=expected_std, 
                                  calc=calculated_std,
                                  arry=test_array))
        assert math.isclose(expected_std, calculated_std), assert_message
    def sample_ddof_1():
        # The test array.
        test_array = np.array([92, 9, 43, 72, 64, 33, 15, 33, 20, 71, 
                               69, 51, 23, 61, 70, 27, 85, 10, 60, 36])
        # The expected value: 2 sqrt(15529/95)
        expected_std = decimal.Decimal('25.570542262121610478833689789632')
        # Calculating.
        calculated_std = mono.math.statistics.standard_deviation(
            array=test_array, ddof=1)
        
        # Check.
        assert_message = ('Expected a standard deviation of `{expt}`, '
                          'calculated is `{calc}`. Array is: {arry}'
                          .format(expt=expected_std, 
                                  calc=calculated_std,
                                  arry=test_array))
        assert math.isclose(expected_std, calculated_std), assert_message

    # Execute the tests
    population_ddof_0()
    sample_ddof_1()

    # All done.
    return None
# Aliases
def test_std(): return test_standard_deviation()