
"""
Very common functions that can be seen as to apply to all arrays.
"""

import numpy as np
import inspect

import sparrowmonolith as mono

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
    else:
        # It cannot be turned into an array.
        raise mono.DataError("Type `{ty}` cannot be turned into a Numpy "
                             "array."
                             .format(ty=type(array_like)))

    # Return and done.
    return array

def change_dtype(array, dtype):
    """ This function turns any array's dtype into the type provided
    as the input. If it does not work, an exception is raised. The
    original array is not affected.

    Parameters
    ----------
    array : array-like
        The array that all of the elements of will be transformed 
        to the new type.
    dtype : type
        The type that all of the elements of the array will become.
    
    Return
    ------
    typed_array : ndarray
        The array where all of the elements are the type provided.
    """
    # Check that the dtype is a legitimate type.
    if (not inspect.isclass(dtype) or inspect.isfunction(dtype)):
        raise mono.TypeError("The dtype is not a class or function that "
                             "can be used as a new type.")
    else:
        # This allows support of both classes and 1 parameter
        # functions.
        dtype_f = lambda x: dtype(x)
        # Convert and return.
        return np.array(list(map(dtype_f, to_array(array).tolist())))

    # The code should not get here.
    raise mono.BrokenLogicError
    return None
