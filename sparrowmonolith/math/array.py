
"""
This module deals with computations done on arrays. The methods
here are used because they are fast implementations, or they 
afford some advantages than the default methods.
"""

import decimal
import numpy as np
import sympy as sy


def to_array(array_like):
    """ This function enforces that the input is translated into
    a numpy array. If it already an array, it is untouched, 
    otherwise it is turned into the closest array-like object.

    Parameters
    ----------
    array_like : array-like
        The array-like data object that will be interpreted into an
        array.
    
    Returns
    -------
    array : ndarray or array-like
        An array object that is more or less compatible with 
        what is expected with Numpy arrays.
    """

    # Find the type of the array-like and convert it based on said
    # type to the most accurate parallel.

    # If it is already an array, then there is no need to continue.
    if (isinstance(array_like, np.ndarray)):
        # For naming convention.
        array = array_like
    # A Python list or tuple is simple to convert to an array.
    elif (isinstance(array_like, (list, tuple))):
        # A simple conversion is justified.
        array = np.array(array_like)



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
    string_array = np.array(to_array(array), dtype=str)

    # Iterate over the array and multiply its value to the product.
    # For efficiency, a running product is used (hence the product
    # starts at 1)
    product = decimal.Decimal('1')
    for multiplierdex in np.nditer(string_array, op_flags=['readonly']):
        product = product * decimal.Decimal(str(multiplierdex))

    # All of the multipliers should have been applied. 
    return product