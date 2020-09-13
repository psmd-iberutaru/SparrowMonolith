
"""
This section is dedicated to functions that are common across all
masking routines.
"""

import numpy as np

import sparrowmonolith as mono

def combine_masks_lor(*args, **kwargs):
    """ This is a function to combine many masks into one single 
    mask. This function does not take any keyword arguments. All of 
    the masks must be the same size. (In general, the first mask is 
    considered the correct mask.)

    This function combines masks by a logical or; for logical and,
    see mono.mask.combine_masks_land().

    Parameters
    ----------
    *args : list
        This should be a collection of array based masks.
    **kwargs : dictionary
        This catches any keyword arguments sent through. An error
        will be raised if any are sent.
        
    Returns
    -------
    combined_mask : array
        The combined mask made of all of the inputted masks.
    """

    # Check for any keyword arguments. There should be none.
    if (len(kwargs) > 0):
        raise mono.DevelopmentError("There should be no keyword argument "
                                    "inputs into this synthesizing "
                                    "function.")
    # If there is only one input array, there is no real synthesis.
    if (len(args) == 0):
        mono.error(mono.InputError,
                   ("There are no input masks to combine, "
                    "returning None."))
        return None
    elif (len(args) == 1):
        mono.warn(mono.InputWarning,
                  ("There is only one input mask, synthesizing is "
                   "not needed."))
        return np.as_array(*args, dtype=bool)
    else:
        # It is assumed that there are masks to combine.
        # Assume that the first mask is the correct size and shapes, 
        # and shall be the template.
        combined_mask = np.zeros_like(args[0], dtype=bool)
        correct_size = combined_mask.size
        correct_shape = combined_mask.shape
        for maskdex, index in zip(args, range(len(args))):
            # Numpy conversion.
            mask_array = np.array(maskdex, dtype=bool)
            # Test for the size and shape.
            if (mask_array.shape != correct_shape):
                raise mono.DataError("The {num}th mask is not the correct "
                                     "shape. Correct shape:  {corr_shp}  "
                                     "Nth shape: {curr_shp}"
                                     .format(num=index, 
                                             corr_shp=correct_shape,
                                             curr_shp=mask_array.shape))
            if (mask_array.size != correct_size):
                mono.error(mono.DataError,
                           ("The {num}th mask is not the correct size. "
                            "Correct size:  {corr_sze}  "
                            "Nth size: {curr_sze}"
                            .format(num=index, corr_sze=correct_shape, 
                                    curr_sze=mask_array.shape)))
            # Otherwise, combine the two masks.
            combined_mask = np.logical_or(combined_mask, mask_array)
        # Finished with synthesizing.
        return combined_mask

    # The program should not reach here as it should have been caught
    # by the else.
    raise mono.BrokenLogicError
    return None

def combine_masks_land(*args, **kwargs):
    """ This is a function to combine many masks into one single 
    mask. This function does not take any keyword arguments. All of 
    the masks must be the same size. (In general, the first mask is 
    considered the correct mask.)

    This function combines masks by a logical and; for logical or,
    see mono.mask.combine_masks_lor().

    Parameters
    ----------
    *args : list
        This should be a collection of array based masks.
    **kwargs : dictionary
        This catches any keyword arguments sent through. An error
        will be raised if any are sent.
        
    Returns
    -------
    combined_mask : array
        The combined mask made of all of the inputted masks.
    """

    # Check for any keyword arguments. There should be none.
    if (len(kwargs) > 0):
        raise mono.DevelopmentError("There should be no keyword argument "
                                    "inputs into this synthesizing "
                                    "function.")
    # If there is only one input array, there is no real synthesis.
    if (len(args) == 0):
        mono.error(mono.InputError,
                   ("There are no input masks to combine, "
                    "returning None."))
        return None
    elif (len(args) == 1):
        mono.warn(mono.InputWarning,
                  ("There is only one input mask, synthesizing is "
                   "not needed."))
        return np.as_array(*args, dtype=bool)
    else:
        # It is assumed that there are masks to combine.
        # Assume that the first mask is the correct size and shapes, 
        # and shall be the template.
        combined_mask = np.ones_like(args[0], dtype=bool)
        correct_size = combined_mask.size
        correct_shape = combined_mask.shape
        for maskdex, index in zip(args, range(len(args))):
            # Numpy conversion.
            mask_array = np.array(maskdex, dtype=bool)
            # Test for the size and shape.
            if (mask_array.shape != correct_shape):
                raise mono.DataError("The {num}th mask is not the correct "
                                     "shape. Correct shape:  {corr_shp}  "
                                     "Nth shape: {curr_shp}"
                                     .format(num=index, 
                                             corr_shp=correct_shape,
                                             curr_shp=mask_array.shape))
            if (mask_array.size != correct_size):
                mono.error(mono.DataError,
                           ("The {num}th mask is not the correct size. "
                            "Correct size:  {corr_sze}  "
                            "Nth size: {curr_sze}"
                            .format(num=index, corr_sze=correct_shape, 
                                    curr_sze=mask_array.shape)))
            # Otherwise, combine the two masks.
            combined_mask = np.logical_and(combined_mask, mask_array)
        # Finished with synthesizing.
        return combined_mask

    # The program should not reach here as it should have been caught
    # by the else.
    raise mono.BrokenLogicError
    return None