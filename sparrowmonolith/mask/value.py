

"""
This contains all of the value based masks. These masks are created
based on the value of the array entries.
"""

import numpy as np
import numpy.ma as np_ma
import decimal

import sparrowmonolith as mono

def mask_sigma_value(data_array, sigma_multiple, sigma_iterations=1):
    """
    This applies a mask on values outside a given multiple of a 
    sigma value.
    
    This function masks values if they are outsize of a sigma range 
    from the mean. The mean and sigma values are automatically 
    calculated from the array provided. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    sigma_multiple : float or array-like
        The multiple of sigma which will be applied. Unequal 
        bottom-top bounds may be set as a list-like input. The 
        first element is the bottom bound; the last element is the 
        top bound.
    sigma_iterations : int
        The number of iterations this filler will run through to
        develop the proper mask.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """
    # It does not make sense to run this mask with no iterations.
    if (sigma_iterations < 1):
        raise mono.InputError("It does not make sense to do this "
                              "mask with less than 1 iteration.")

    # Check if the sigma limits are the same, or the user 
    # provided for a lower and upper sigma to use.
    if (isinstance(sigma_multiple,(int,float))):
        # It is just a number, apply them evenly.
        bottom_sigma_multiple = sigma_multiple
        top_sigma_multiple = sigma_multiple
    elif (np.array(sigma_multiple).size == 1):
        # It is likely that this is a single number, but just 
        # embedded in an array.
        flat_sigma_multiple = np.squeeze(np.array(sigma_multiple))
        bottom_sigma_multiple = flat_sigma_multiple
        top_sigma_multiple = flat_sigma_multiple
    else:
        # The sigma multiple is most likely some sort of array for 
        # uneven values.
        flat_sigma_multiple = np.squeeze(np.array(sigma_multiple))
        bottom_sigma_multiple = flat_sigma_multiple[0]
        top_sigma_multiple = flat_sigma_multiple[-1]

    # The number of iterations are accomplished by just doing loops.
    final_mask = mono.mask.mask_nothing(data_array=data_array)
    for iterdex in range(sigma_iterations):
        # Calculate the mean and the sigma values of the data array.
        # masked values mean it was caught in previous iterations.
        mean = mono.math.statistics.arithmetic_mean(
            array=np_ma.array(data_array, mask=final_mask).compressed())
        stddev = mono.math.statistics.standard_deviation(
            array=np_ma.array(data_array, mask=final_mask).compressed())
        
        # Calculating the two individual masks and combining them.
        min_mask = mask_minimum_value(
            data_array=data_array, 
            minimum_value=(mean - stddev * bottom_sigma_multiple))
        max_mask = mask_maximum_value(
            data_array=data_array, 
            maximum_value=(mean + stddev * top_sigma_multiple))
        
        # The mask based version is proper, the difference between a 
        # mask and a mask is just semantics. Also, keep track
        # of the previous masks all run through the iterations.
        final_mask = mono.mask.common.synthesize_masks(
            final_mask, min_mask, max_mask)

    return final_mask

def mask_percent_truncation(data_array, top_percent, bottom_percent):
    """ This mask truncates the top and bottom percent of values 
    provided.

    The values ``top_percent`` and ``bottom_percent`` notate the 
    percentage of values from top and bottom of the data array 
    (in number of values) that should be masked. The values masked 
    are independent on the previous masks applied.

    If the percentage of values leads to a non-integer number of
    values to be masked or where many of the same value is present,
    values are kept.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    top_percent : float
        The percent of values from the top (highest value) of 
        the array that is to be masked. Must be between 0 and 1.
    bottom_percent : float
        The percent of values from the bottom (lowest value) of 
        the array that is to be masked. Must be between 0 and 1.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """
    # For higher precision, in a way. It also gets around rounding
    # errors for the percentile to count conversion.
    n_data_points = int(np.size(data_array))
    top_percent = decimal.Decimal(str(top_percent))
    bottom_percent = decimal.Decimal(str(bottom_percent))
    ONE = decimal.Decimal('1.0')

    # Ensure that they are percentages.
    if (not (0 <= top_percent <= 1)):
        raise mono.InputError("The top percent must be between 0 and 1.")
    if (not (0 <= bottom_percent <= 1)):
        raise mono.InputError("The bottom percent must be between 0 and 1.")

    # The percentage cuts are just fancy count cuts. We will apply
    # them as so.
    top_count = np.floor(top_percent * n_data_points)
    bottom_count = np.floor(bottom_percent * n_data_points)
    # We rely on the mask count truncation being kept.
    final_mask = mask_count_truncation(data_array=data_array, 
                                       top_count=top_count, 
                                       bottom_count=bottom_count)
    # Finally return
    return final_mask

def mask_count_truncation(data_array, top_count, bottom_count):
    """ This mask truncates the top and bottom number of discrete 
    values.

    The values ``top_count`` and ``bottom_count`` notate the number 
    of values from top and bottom of the data array (in value) that 
    should be cut. The values masked are independent on the 
    previous masks applied.

    If the cutoff point has multiple entries of the same value,
    they are kept.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    top_count : int
        The number of values from the top (highest value) of the 
        array that is to be masked.
    bottom_count : int
        The number of values from the bottom (lowest value) of the 
        array that is to be masked.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """
    
    # Simple type checking as the top count and bottom count
    # are used for indexing.
    top_count = int(top_count)
    bottom_count = int(bottom_count)

    # Sort the data so that the indexes line with order.
    sorted_data = np.sort(data_array, axis=None)
    len_sorted_data = len(sorted_data)

    
    # Find the values above and below the cuts, simplifying the 
    # process to pure value cuts. However, some special cases needs
    # to be taken care of.
    if ((top_count + bottom_count) >= len_sorted_data):
        # They are masking out their entire array, or more.
        return mono.mask.mask_everything(data_array=data_array)
    else:
        # Calculate the mask cuts.
        # Upper mask cuts.
        try:
            upper_value = sorted_data[:-top_count][-1]
        except TypeError:
            # The splicing failed, find out why.
            if (top_count <= 0):
                # They don't want to cut the top.
                upper_value = np.minimum(sorted_data) - 1
            elif (top_count >= len_sorted_data):
                # They want to mask the entire array from the top.
                # But it should have been caught earlier.
                raise mono.BrokenLogicError("This should have been caught "
                                            "by the full mask function.")
            else:
                # The error is unknown.
                raise mono.DevelopmentError("Why did the top count fail? "
                                            "Top count: {top_c}"
                                            .format(top_c=top_count))
        # Lower mask cuts.
        try:
            lower_value = sorted_data[bottom_count:][0]
        except TypeError:
            # The splicing failed, find out why.
            if (bottom_count <= 0):
                # They don't want to cut the top.
                upper_value = np.minimum(sorted_data) - 1
            elif (bottom_count >= len_sorted_data):
                # They want to mask the entire array from the top.
                # But it should have been caught earlier.
                raise mono.BrokenLogicError("This should have been caught "
                                            "by the full mask function.")
            else:
                # The error is unknown.
                raise mono.DevelopmentError("Why did the top count fail? "
                                            "Top count: {top_c}"
                                            .format(top_c=top_count))

        # Calculating the two individual masks and combining them.
        max_mask = mask_maximum_value(data_array=data_array, 
                                      maximum_value=upper_value)
        min_mask = mask_minimum_value(data_array=data_array, 
                                      minimum_value=lower_value)
        # The mask based version is proper, the difference between a 
        # mask and a mask is just semantics.
        final_mask = mono.mask.synthesize_masks(min_mask, max_mask)
        return final_mask
    # The code should not reach here.
    raise mono.BrokenLogicError
    return None

def mask_maximum_value(data_array, maximum_value):
    """ This function computes a mask for all values 
    strictly more than some maximum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    maximum_value : float
        The value that data values strictly more than will be 
        tagged as masked.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """
    # Find which values are strictly less than. Decimal allows for
    # higher precision.
    final_mask = np.where(data_array > maximum_value, True, False)

    # Done
    return final_mask

def mask_minimum_value(data_array, minimum_value):
    """ This function computes a mask for all values 
    strictly less than some minimum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    minimum_value : float
        The value that data values strictly less than will be 
        tagged as masked.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """
    # Find which values are strictly less than.
    final_mask = np.where(data_array < minimum_value, True, False)

    # Done
    return final_mask

def mask_exact_value(data_array, exact_value):
    """ This function computes a mask for all values 
    equal to some exact value.

    Float equality comparisons are dependent on tolerances. The main
    back function used is `numpy.isclose`.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    exact_value : float
        The value that data values close will be tagged as masked.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """

    # For usage in the close comparison, a filled array. 
    exact_value_array = np.full_like(data_array, exact_value)

    # Find which values are close.
    final_mask = np.isclose(data_array, exact_value_array)

    # Done
    return final_mask
