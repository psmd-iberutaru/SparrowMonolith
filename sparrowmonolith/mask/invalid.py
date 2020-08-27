
"""
These mask functions mask based on if the values of the arrays
are considered invalid, or just not within the normal real number
line (such as infinity and NaN).
"""

import numpy as np
import numpy.ma as np_ma


def mask_invalid_all(data_array):
    """ This masks all invalid data, as defined by the other
    masking functions in this field.

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
    pass

    return None


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