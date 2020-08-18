
""" 
This is a module that is dedicated to mathematical functions that
are commonly used.
"""

import numpy as np
import astropy as ap
import astropy.modeling as ap_mod

import sparrowmonolith as mono

def gaussian_function(input, mean, stddev, amplitude):
    """ This is a wrapper function around Astropy's Gaussian
    function. This takes the input of a function, and gives it an
    output according to the Gaussian parameters provided. The 
    function itself is also returned.

    Parameters
    ----------
    input : array
        The input into the Gaussian function.
    mean : float
        The mean of the Gaussian function.
    stddev : float
        The standard deviation of the Gaussian function.
    amplitude : float
        The amplitude to of the Gaussian function.
    
    Returns
    -------
    output : array
        The output when the Gaussian function is calculated from the 
        input.
    gaussian_function : function
        The Gaussian function with the parameters provided already
        given.
    """

    # The Gaussian function itself.
    def gaussian_model(x=None, mean=0, stddev=0, amplitude=0):
        # A wrapper around Astropy's.
        gaussian = ap_mod.models.Gaussian1D(amplitude=amplitude, mean=mean,
                                            stddev=stddev)
        # Evaluation.
        output = gaussian.evaluate(x, amplitude=amplitude, 
                                   mean=mean, stddev=stddev)
        # Return
        return output

    # Return both the function and its evaluation.
    gaussian_function = lambda x: gaussian_model(
        input=mono.math.array.to_array(x), 
        mean=mean, stddev=stddev, amplitude=amplitude)
    try:
        output = gaussian_function(x=input)
    except Exception:
        mono.warn(mono.DataError,
                  ("Could not compute the output of the Gaussian function."))
        output = None

    # All done.
    return output, gaussian_function