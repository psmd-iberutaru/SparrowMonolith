
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
    one of the better nights of the year.) Arrays are supported,
    single values have some level of higher precision. 

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
        # Convert all of the angles to degrees and arrays for 
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
    if (np.where((-PI_HALF < target_dec) & (target_dec < PI_HALF), 
                 False, True).any()):
        # Target declinations are outside +/- pi/2 radians.
        raise mono.InputError("There exists at least one target declination "
                              "outside the polar limits of +/- pi/2. "
                              "Target declinations: {t_dec}"
                              .format(t_dec=target_dec))
    if (np.where((-PI_HALF < obs_latitude) & (obs_latitude < PI_HALF), 
                 False, True).any()):
        # Observatory latitudes are outside +/- pi/2 radians.
        raise mono.InputError("There exists at least one observatory "
                              "latitude outside the polar limits "
                              "of +/- pi/2. "
                              "Observatory latitudes: {o_lat}"
                              .format(o_lat=obs_latitude))
    if (np.where((ZERO < minimum_alt) & (minimum_alt < PI_HALF), 
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
    # See Sparrow's Notes <TITLE> for more information.
    with mono.silence_specific_warning(RuntimeWarning):
        radians_observeable = 2 * np.arccos(
            ((np.sin(minimum_alt) - np.sin(obs_latitude)*np.sin(target_dec)) 
             / (np.cos(obs_latitude)*np.cos(target_dec))))

        # If and where the trigonometry fails, that means that the 
        # observable time is less than 0 hours, round up to zero.
        radians_observeable = np.nan_to_num(radians_observeable, 
                                            nan=0, posinf=24, neginf=0)

    # Convert the radian angle result to units of hours 
    # via 1 hr = 15 deg = pi/12 rad. (The declination dependence was
    # already accounted for in the previous equation.)
    if (isinstance(radians_observeable, float)):
        # A single value can be afforded higher accuracy as there
        # is no Numpy to intercept it and give TypeErrors.
        rad_to_hour_factor = sy.N(12 / sy.pi, precision)
    else:
        rad_to_hour_factor = 12 / np.pi
    # Convert.
    hours_observeable = radians_observeable * rad_to_hour_factor
    # Sanity check and all done.
    assert np.all(hours_observeable <= 24), "Too many hours in a day."
    return hours_observeable
