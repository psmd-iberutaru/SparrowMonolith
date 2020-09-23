
"""
This module deals with observational astronomy and telescope 
calculators.
"""

import decimal
import numpy as np
import sympy as sy

import sparrowmonolith as mono

def maximum_time_observable(target_dec, obs_latitude, minimum_alt, 
                            angle_unit='radian'):
    """ This function returns the maximum duration of time, in 
    hours, of how long an astronomical object can be observed over 
    some minimum altitude. (The day of observation is assumed to be
    one of the better nights of the year.) Arrays are supported.

    Parameters
    ----------
    target_dec : float
        The declination of the observing target. It must be in the 
        angular units specified by `angle_unit`. 
    obs_latitude : float
        The latitude of the observer (i.e. telescope) on the Earth.
        It must be in the angular units specified by `angle_unit`. 
    minimum_alt : float 
        The minimum altitude that the object must be above to be 
        considered observable. This is mostly used for observing
        above a given airmass. It must be in the angular units 
        specified by `angle_unit`.
    angle_unit : string (optional)
        The unit of angle that the values are inputted as; it can
        be either `radian` for radians or `degree` for degrees.

    Return
    ------
    hours_observeable : float
        The number of hours that the target is considered 
        observable. The hours are in decimal form.
    """
    # Convert the angles to radians as that is what Numpy natively 
    # uses.
    angle_unit = str(angle_unit).lower()
    if (angle_unit == 'radian'):
        # The angles are already in radians, there is no need for 
        # conversion. But, still use Numpy arrays for broadcasting.
        target_dec = np.array(target_dec)
        obs_latitude = np.array(obs_latitude)
        minimum_alt = np.array(minimum_alt)
    elif (angle_unit == 'degree'):
        # Convert all of the angles to radians and arrays for 
        # broadcasting.
        target_dec = np.deg2rad(target_dec)
        obs_latitude = np.deg2rad(obs_latitude)
        minimum_alt = np.deg2rad(minimum_alt)
    else:
        # The angle unit is unknown.
        raise mono.InputError("The angular unit provided is not a valid "
                              "angular unit for this function. Accepted "
                              "units are: `radian`, `degree`")

    # Double check that the angular measurements falls within
    # physical boundaries. (Using decimal/sympy for 
    # higher numerical precision.)
    precision = 20
    ZERO = decimal.Decimal('0')
    PI_HALF = decimal.Decimal(str(sy.N(sy.pi/2, precision)))
    if (np.where((-PI_HALF <= target_dec) & (target_dec <= PI_HALF), 
                 False, True).any()):
        # Target declinations are outside +/- pi/2 radians.
        raise mono.InputError("There exists at least one target declination "
                              "outside the polar limits of +/- pi/2. "
                              "Target declinations: {t_dec}"
                              .format(t_dec=target_dec))
    if (np.where((-PI_HALF <= obs_latitude) & (obs_latitude <= PI_HALF), 
                 False, True).any()):
        # Observatory latitudes are outside +/- pi/2 radians.
        raise mono.InputError("There exists at least one observatory "
                              "latitude outside the polar limits "
                              "of +/- pi/2. "
                              "Observatory latitudes: {o_lat}"
                              .format(o_lat=obs_latitude))
    if (np.where((ZERO <= minimum_alt) & (minimum_alt <= PI_HALF), 
                 False, True).any()):
        # Minimum altitudes are outside 0 to pi/2 radians.
        raise mono.InputError("There exists at least one minimum altitude "
                              "outside the horizon-zenith limits "
                              "of 0 to +pi/2. "
                              "Minimum altitudes: {m_alt}"
                              .format(m_alt=minimum_alt))

    # Using an equation to compute the maximum time observable. 
    # This equation comes from using Equatorial in AltAz and finding
    # the limiting hour angles on both sides of the meridian. 
    # See ``Sparrow's Notes Maximum Astronomical Observing Time``
    # for more information.
    def _extended_arccos_function(input):
        """ The arccos function is only defined between a domain of
        0 <= x <= 1. However, the internal value of this arccos 
        lends itself to have input values outside of this range.
        This arccos extension applies the physical meaning that 
        if an input of less than -1 is given, the target has an 
        observing time of 24 hours; if it has an input greater 
        than 1, it has an observing time of 0 hours. Justification  
        is not mathematical, but physical; out math's logical limits.
        """
        # Array for broadcasting
        input = np.asarray(input)
        output = np.zeros_like(input)
        # Calculate the arccos, deal with the unique values after.
        with mono.silence_specific_warning(RuntimeWarning):
            output = np.arccos(input)
        # Internal value less than -1 --> 24 hours ~~> pi rad one HA.
        output[np.asarray(input <= -1).nonzero()] = np.pi
        # Internal value more than 1 --> 0 hours ~~> 0 rad one HA.
        output[np.asarray(1 <= input).nonzero()] = 0
        # Retain the higher precision where possible.
        return output
    # Calculate the angular observable duration.
    _internal = ((np.sin(minimum_alt) - np.sin(obs_latitude) 
                  * np.sin(target_dec))
                / (np.cos(obs_latitude)*np.cos(target_dec)))
    radians_observeable = 2 * _extended_arccos_function(input=_internal)

    # Convert the radian angle result to units of hours 
    # via 1 hr = 15 deg = pi/12 rad. (The declination dependence was
    # already accounted for in the previous equation.)
    hours_observeable = radians_observeable * (12 / np.pi)
    # Sanity check and all done.
    assert np.all(hours_observeable <= 24), "Too many hours in a day."
    return hours_observeable
