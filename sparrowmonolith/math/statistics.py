
"""
This module is made for the complete computation of statistical
results.
"""

import decimal
import numpy as np
import copy

import sparrowmonolith as mono

# Means and averages
##########

def arithmetic_mean(array):
    """ This computes the arithmetic mean of a data array. This is
    mostly a wrapper around the Numpy function. Arbitrary precision
    is supported.

    Parameters
    ----------
    array : array-like
        The array of data that will have its arithmetic mean
        calculated.

    Returns
    -------
    result : Decimal
        The arithmetic mean of the array.
    """
    # Using Decimal will allow for "arbitrary precision", change
    # to using Numpy arrays.
    array = np.array(array, dtype=decimal.Decimal).flatten()
    # Calculating the mean.
    summation = sum(array)
    N = decimal.Decimal(array.size)
    result = summation / N
    # All done.
    return result
# Aliases
mean = arithmetic_mean


def median(array):
    """ This returns the median of an array. This is a wrapper 
    around a sort and average function.

    Here, the median is defined as the middle value of a sorted 
    array, if the array is even in length, the average of the two
    middle points is used.

    Arbitrary precision is supported.

    Parameters
    ---------
    array : array-like
        The array of data that will have its median calculated.

    Returns
    -------
    result : Decimal
        The median of the array.
    """
    # Sort the 'list'.
    sort_array = sorted(np.array(array).flatten())
    # Return the middle result, or the mean of the two results.
    N = len(sort_array)
    if (N % 2):
        # Odd, just return the middle.
        index = (N - 1) // 2
        return sort_array[index]
    else:
        # Even, return the average of the middle two.
        index = (N - 1) // 2
        return arithmetic_mean(array=sort_array[index:index+2])
    # Should not reach here.
    raise mono.BrokenLogicError
    # All done.
    return None


# Standard deviation
def standard_deviation(array, ddof=0):
    """ This computes the standard deviation of the array. It is
    a wrapper around np.std. Arbitrary precision is supported.

    Parameters
    ----------
    array : array-like
        The data that the standard deviation will be calculated 
        from.
    ddof : int (optional)
        Means Delta Degrees of Freedom. The divisor used in 
        calculations is N - ddof, where N represents the number of 
        elements. By default ddof is zero.


    Returns
    -------
    result : float
        The standard deviation.
    """
    # Using Decimal will allow for "arbitrary precision", change
    # to using Numpy arrays.
    array = np.array(array, dtype=decimal.Decimal).flatten()

    # Ca lculating the std.
    mean = arithmetic_mean(array)
    total_of_delta_squared = sum((array - mean)**2)
    divisor = len(array) - ddof

    # The std itself
    result = decimal.Decimal(total_of_delta_squared / divisor).sqrt()
    # All done.
    return result
# Aliases
std = standard_deviation