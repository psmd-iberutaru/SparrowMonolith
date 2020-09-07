
"""
These mask functions mask based on if the values of the arrays
are considered invalid, or just not within the normal real number
line (such as infinity and NaN).
"""

import numpy as np
import numpy.ma as np_ma
import inspect

import sparrowmonolith as mono

def mask_invalid_all(data_array):
    """ This masks all invalid data, as defined by the other
    masking functions in this field. This is a wrapper function
    that calls all other invalid functions.

    Parameters
    ----------
    data_array : ndarray
        The array of which the invalid data will be masked.

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """
    # Find the file within this module with all of the invalid 
    # masks.
    try:
        self_filename = 'mask/invalid.py'
        self_pathname = mono.meta.find_file_in_directory(
            directory=mono.meta.get_module_directory(module=mono), 
            filename=self_filename, throw=False)
    except mono.AmbiguousError:
        raise mono.AssumptionError("There is more than one matching "
                                   "invalid.py file. More strict file "
                                   "matching names needs to be applied.")
    # Load the file.
    invalid_module = mono.meta.load_module_file(pathname=self_pathname)

    # Get all of the invalid mask functions.
    mask_invalid_function_dict = inspect.getmembers(
        invalid_module, inspect.isfunction)
    # Remove all functions that are not masking functions, also 
    # remove this function itself to prevent an infinite loop.
    invalid_masking_functions = []
    for keydex, functiondex in dict(mask_invalid_function_dict).items():
        if (not ('mask' in keydex)):
            # This function does not belong.
            continue
        elif (keydex == 'mask_invalid_all'):
            # Do not include this own function to prevent infinite
            # looping.
            continue
        else:
            # A valid function.
            invalid_masking_functions.append(functiondex)

    # Run through all of the masking functions and combine all of 
    # them until done.
    # Initial mask.
    final_mask = mono.mask.mask_nothing(data_array=data_array)
    for functiondex in invalid_masking_functions:
        final_mask = mono.mask.synthesize_masks(
            final_mask, functiondex(data_array=data_array))
    # All done.
    return final_mask




def mask_invalid_infinity(data_array):
    """ This mask applies a mask to all infinite values as defined
    by np.inf and -np.inf. 
    
    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """
    # This mask is, in a way, a wrapper around the Numpy 
    # functionality.
    final_mask = np.array(np.isinf(data_array), dtype=bool)
    return final_mask

def mask_invalid_positive_infinity(data_array):
    """ This mask applies a mask to all infinite values as defined
    by np.inf. 
    
    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """
    # This mask is, in a way, a wrapper around the Numpy 
    # functionality.
    final_mask = np.array(np.isposinf(data_array), dtype=bool)
    return final_mask

def mask_invalid_negetive_infinity(data_array):
    """ This mask applies a mask to all infinite values as defined
    by -np.inf. 
    
    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """
    # This mask is, in a way, a wrapper around the Numpy 
    # functionality.
    final_mask = np.array(np.isneginf(data_array), dtype=bool)
    return final_mask

def mask_invalid_nan(data_array):
    """ This mask applies a mask to mask all of the NaN or 
    None values from the data array. Both Numpy and Python None/NaNs
    are masked by this mask.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """
    # This mask is, in a way, a wrapper around the Numpy 
    # functionality.
    final_mask = np.array(np.isnan(data_array), dtype=bool)
    return final_mask