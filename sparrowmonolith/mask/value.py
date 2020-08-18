

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
    This applies a mask on pixels outside a given multiple of a sigma 
    value.
    
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
    final_mask = mono.mask_nothing(data_array=data_array)
    for iterdex in range(sigma_iterations):
        # Calculate the mean and the sigma values of the data array.
        # masked pixels mean it was caught in previous iterations.
        mean = mono.math.ifas_robust_mean(
            array=np_ma.array(data_array, mask=final_mask).compressed())
        stddev = mono.math.ifas_robust_std(
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
        final_mask = mono.mask.base.synthesize_masks(final_mask, 
                                                     min_mask, max_mask)

    return final_mask

def mask_percent_truncation(data_array, top_percent, bottom_percent):
    """ This mask truncates the top and bottom percent of pixels 
    provided.

    The values ``top_percent`` and ``bottom_percent`` notate the 
    percentage of pixels from top and bottom of the data array 
    (in value) that should be masked. The pixels masked are 
    independent on the previous masks applied.

    If the percentage of pixels leads to a non-integer number of
    pixels to be masked, the number is floored. All pixels that have
    a same value as the limiting pixel value for the top and bottom
    percent of pixels are also masked.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    top_count : float
        The percent of pixels from the top (highest value) of 
        the array that is to be masked.
    bottom_count : int
        The percent of pixels from the bottom (lowest value) of 
        the array that is to be masked.

    Returns
    -------
    final_mask : ndarray
        The mask as computed by this function.
    """
    # For higher precision, in a way.
    top_percent = np.longdouble(top_percent)
    bottom_percent = np.longdouble(bottom_percent)
    ONE = np.longdouble(1.0)

    # A percent truncation is a fancy pixel truncation, and is 
    # going to be applied as such. 
    total_n_pixels = int(data_array.size)
    top_pixel = int(np.floor(total_n_pixels * top_percent))
    bottom_pixel = int(np.floor(total_n_pixels * bottom_percent))

    # The pixel mask
    final_mask = mask_pixel_truncation(data_array=data_array, 
                                       top_count=top_pixel, 
                                       bottom_count=bottom_pixel)

    # The above method requires that the total number of pixels is 
    # not comparable to the float resolution. If not, then lower 
    # bound values will be improperly cut and percentages will not 
    # be accurately calculated.
    if (np.log10(total_n_pixels) 
        > (- np.log10(np.finfo(np.longdouble).resolution) - 5)):
        mono.warn(mono.ImprecisionWarning,
                  ("Float multiplication is used to calculate truncations. "
                   "The total number of pixels approaches the machine "
                   "resolution for multiplication."))
    elif (np.log10(total_n_pixels) 
          > (- np.log10(np.finfo(np.longdouble).resolution))):
        mono.error(mono.ImprecisionError,
                   ("Current number of pixels exceeds resolution of float "
                    "multiplication; percent truncation may be wildly "
                    "inaccurate."))
    # Finally return
    return final_mask

def mask_pixel_truncation(data_array, top_count, bottom_count):
    """ This mask truncates the top and bottom number of pixels 
    provided.

    The values ``top_count`` and ``bottom_count`` notate the number 
    of pixels from top and bottom of the data array (in value) that 
    should be cut. The pixels masked are independent on the 
    previous masks applied.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    top_count : int
        The number of pixels from the top (highest value) of the 
        array that is to be masked.
    bottom_count : int
        The number of pixels from the bottom (lowest value) of the 
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
    sorted_data = np.sort(np_ma.getdata(data_array, subok=False), axis=None)

    
    # Find the values above and below the cuts, simplifying the 
    # process to pure value cuts.
    upper_value = sorted_data[:-top_count][-1]
    bottom_value = sorted_data[bottom_count:][0]

    # Calculating the two individual masks and combining them.
    max_mask = mask_maximum_value(data_array=data_array, 
                                  maximum_value=upper_value)
    min_mask = mask_minimum_value(data_array=data_array, 
                                  minimum_value=bottom_value)
    # The mask based version is proper, the difference between a 
    # mask and a mask is just semantics.
    final_mask = mono.mask.base.synthesize_masks(min_mask, max_mask)

    return final_mask

def mask_maximum_value(data_array, maximum_value):
    """ This function computes a mask for all pixel values 
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
    final_mask = np.where(data_array > decimal.Decimal(maximum_value), 
                          True, False)

    # Done
    return final_mask

def mask_minimum_value(data_array, minimum_value):
    """ This function computes a mask for all pixel values 
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
    final_mask = np.where(data_array < decimal.Decimal(minimum_value), 
                          True, False)

    # Done
    return final_mask

def mask_exact_value(data_array, exact_value):
    """ This function computes a mask for all pixel values 
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
