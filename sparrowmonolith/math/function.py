
""" 
This is a module that is dedicated to mathematical functions that
are commonly used.
"""

import numpy as np
import astropy as ap
import astropy.modeling as ap_mod

import sparrowmonolith as mono

def gaussian_function(mean, stddev, amplitude):
    """ This is a wrapper function around Astropy's Gaussian
    function. It returns a function in the form of f(x) = y for a
    Gaussian function based on the parameters provided.

    Parameters
    ----------
    mean : float
        The mean of the Gaussian function.
    stddev : float
        The standard deviation of the Gaussian function.
    amplitude : float
        The amplitude to of the Gaussian function.
    
    Returns
    -------
    gaussian_function : function
        The Gaussian function with the parameters provided already
        given.
    """

    # The Gaussian function itself.
    def _gaussian_model(input=None, mean=0, stddev=0, amplitude=0):
        # A wrapper around Astropy's.
        gaussian = ap_mod.models.Gaussian1D(
            amplitude=amplitude, mean=mean, stddev=stddev)
        # Evaluation.
        output = gaussian.evaluate(input, amplitude=amplitude, 
                                   mean=mean, stddev=stddev)
        # Return
        return output

    # Return the function with the parameters the user gave.
    gaussian_function = lambda x: _gaussian_model(
        input=x, mean=mean, stddev=stddev, amplitude=amplitude)

    # All done.
    return gaussian_function