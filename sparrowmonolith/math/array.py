
"""
This module deals with computations done on arrays. The methods
here are used because they are fast implementations, or they 
afford some advantages than the default methods.
"""

import decimal
import numpy as np
import sympy as sy

import sparrowmonolith as mono

def integer_array_sum(array):
    """ This produces the summation of an array for integers. 
    Every value is added together, infinite precision should be 
    supported.
    
    Parameters
    ----------
    array : ndarray
        The array by which all the elements will be added together.
    
    Returns
    -------
    total : integer
        The summation of the array.
    """
    # Just go through the array and start adding. Using Python's
    # native infinite precision integers.
    total = int(0)
    for valuedex in np.asarray(array).flatten():
        total = total + int(valuedex)
    return total

def float_array_sum(array):
    """ This produces the summation of an array. Every value is 
    basically added together in this function. High precision is
    supported. 

    Parameters
    ----------
    array : ndarray
        The array by which all the elements will be added together.

    Returns
    -------
    total : float
        The summation of the array.
    """
    # Just go through the entire array and start adding.
    total = decimal.Decimal('0')
    for valuedex in np.asarray(array).flatten():
        total = total + decimal.Decimal(str(valuedex))
    # All done.
    return total


def integer_array_product(array):
    """ This produces the product of every value within an array.
    Sympy is used because of their superior handling of precision 
    compared to Numpy. The array must be integers. If it is not, 
    then they are converted.
    
    Parameters
    ----------
    array : ndarray
        The array by which all elements will be multiplied together.

    Returns
    -------
    product : float
        The product of the multiplication of the array.
    """

    # Reformat the array into a Sympy float array.
    sympy_array = sy.Array(array)
    sympy_array = sympy_array.applyfunc(lambda x: sy.Integer(x))

    # Flatten the array.
    size = len(sympy_array)
    flat_sympy_array = sympy_array.reshape(size)

    # And finally, compute the product.
    product = sy.prod(flat_sympy_array)
    return product

def float_array_product(array):
    """ This produces the product of every value within an array.
    The values may be integers or not, there is some inherent 
    imprecision, but, this function is far more accurate than
    other more simple methods.
    
    This method will return a decimal object.

    Parameters
    ----------
    array : ndarray
        The array by which all elements will be multiplied together.

    Returns
    -------
    product : Decimal
        The product of the multiplication of the array. This returns
        a decimal object.
    """
    # For the highest precision, work with strings for numbers. This 
    # also ensures that array-like objects can be used.
    string_array = np.array(mono.object.array.to_array(array), dtype=str)

    # Iterate over the array and multiply its value to the product.
    # For efficiency, a running product is used (hence the product
    # starts at 1)
    product = decimal.Decimal('1')
    for multiplierdex in np.nditer(string_array, op_flags=['readonly']):
        product = product * decimal.Decimal(str(multiplierdex))

    # All of the multipliers should have been applied. 
    return product