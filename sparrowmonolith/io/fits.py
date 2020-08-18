
"""
This module handles many of the fits file io functions.
"""

import astropy as ap
import astropy.io.fits as ap_fits
import copy
import numpy as np
import os

import sparrowmonolith as mono

# Read and write.
def read_fits_file(filename, extension=0, silent=False):
    """ A function to ensure proper loading/reading of fits files.

    This function, as its name, opens a fits file. It returns the 
    Astropy HDU file. This function is mostly done to ensure that 
    files are properly closed. It also extracts the needed data 
    and header information from the file.

    Parameters
    ---------- 
    filename : string
        This is the path of the file to be read, either relative 
        or absolute.
    extension : int or string (optional)
        The desired extension of the fits file. Defaults to primary 
        structure. 
    silent : boolean (optional)
        Turn off all warnings and information sent by this function 
        and functions below it.

    Returns
    -------
    hdu_object : HDULists
        The Astropy object representing the fits file.
    header : Header
        The Astropy header object representing the headers of the 
        given file.
    data : ndarray
        The Numpy representation of a fits file data.
    """

    # The user doesn't want any warnings.
    if (silent):
        with mono.absolute_silence():
            return read_fits_file(filename=filename, extension=extension,
                                  silent=False)

    with ap_fits.open(filename) as hdul:
        hdu_object = copy.deepcopy(hdul)
        
        # Just because just in case.
        hdul.close()
        del hdul

    # Read from the extension
    header = hdu_object[extension].header
    data = hdu_object[extension].data

    return hdu_object, header, data

def write_fits_file(filename, header, data, hdu_object=None, 
                    save=True, overwrite=False, silent=False):
    """ A function to ensure proper writing of fits files.

    This function writes fits files given the data and header file. 
    The file name should be a complete path and must also include 
    the file name.

    Parameters
    ----------
    filename : string
        This is the path of the file to be written, either relative 
        or absolute.
    header : Header
        The Astropy header object representing the headers of the 
        given file.
    data : ndarray
        The Numpy representation of a fits file data.
    hdu_object : Astropy HDUList (optional)
        An astropy HDUList object, if provided, this object takes 
        priority to be written, the rest are ignored.
    save : boolean (optional)
        If ``True``, then the fits file will be written to file, 
        else, just the instance will be returned.
    overwrite : boolean (optional)
        If ``True``, if there exists a file of the same name, 
        overwrite.
    silent : boolean (optional)
        Turn off all warnings and information sent by this function 
        and functions below it.

    Returns
    -------
    hdul_file : Astropy HDUList
        The file object that was written to disk. If ``hdu_object`` 
        was provided, it is returned untouched.
    """

    # The user does not want any warnings.
    if (silent):
        with mono.absolute_silence():
            return write_fits_file(filename=filename, 
                                   header=header, data=data, 
                                   hdu_object=hdu_object, 
                                   save=save, overwrite=overwrite, 
                                   silent=False)


    # Check if the file name has a fits extension.
    if (mono.string.path.split_pathname(pathname=filename)[2] != '.fits'):
        raise mono.FileError("The filename path `{path}` does not have a "
                             "fits extension. It is not considered a fits "
                             "file."
                             .format(path=filename))


    # Create the main HDUL object to write the fits file.
    # Check for the hdu_object.
    if (isinstance(hdu_object, (ap_fits.PrimaryHDU,ap_fits.HDUList))):
        # Astropy can handle PrimaryHDU -> .fits conversion.
        hdul_file = hdu_object
    else:
        # Else, deal with the data.
        # If the data is a boolean, then as FITS cannot handle 
        # booleans, convert to int.
        if (isinstance(np.ravel(data)[0], (bool, np.bool_))):
            data = np.where(data, 1, 0)

        # The HDU header may be a dictionary, if so, as Astropy can
        # only handle actual header objects, convert.
        if (isinstance(header, dict)):
            header = ap_fits.Header(header)

        # Writing to a fits HDU.
        hdu = ap_fits.PrimaryHDU(data=np.array(data), header=header)
        hdul_file = ap_fits.HDUList([hdu])

    # Check to see if the file exists, if so, then overwrite 
    # if provided for.
    if (os.path.isfile(filename) and (save)):
        if (overwrite):
            # It should be overwritten, warn to be nice. 
            mono.warn(mono.OverwriteWarning,
                      ("There exists a file with the provided "
                       "name. Overwrite is true; the previous "
                       "file will be replaced as provided."))
        else:
            # It should not overwritten at this point.
            raise mono.FileError("There exists a file with the same name as "
                                 "the previous one. Overwrite is set to "
                                 "False, the new fits file cannot be "
                                 "written. File name: {f_name}"
                                 .format(f_name=filename))

    # Write, follow overwrite instructions, assume the user knows 
    # what they are doing. Return object.
    if (save):
        hdul_file.writeto(filename, overwrite=overwrite)

    return hdul_file

# Header manipulation.
def append_header_card(filename, header_cards, comment_cards=None):
    """ This is a function to add header card entries into the 
    header of a fits file. This uses dictionaries to achieve said 
    result.

    Parameters
    ----------
    filename : string
        This is the path of the file to be written, either relative 
        or absolute.
    header_cards : dictionary
        The header entries to be added to the header file. Please 
        note that the keys of the dictionary must be no more than 
        8 characters; otherwise a HIERARCH card will be used.
    comment_cards : dictionary (optional)
        The comment entries to be added to the header file. The 
        keys of the comment dictionary and the `header_cards` must 
        line up.

    Returns
    -------
    None
    """
    # Sort the comment cards to the needed dictionary. If it is 
    # nothing, then a blank dictionary is compatible with no comment.
    comment_cards = (comment_cards if isinstance(comment_cards, dict) 
                     else dict())

    # Add the entries.
    for keydex, valuedex in copy.deepcopy(header_cards).items():
        # Check that the entries are valid type based on the FITS 
        # specification. Astropy does this, but it is not as clear.
        if (isinstance(valuedex, (int, float, str))):
            # This is a valid and accepted type, write to the Header.
            ap_fits.setval(filename, keydex, value=valuedex, 
                           comment=comment_cards.get(keydex,None))
        elif (isinstance(valuedex, bool)):
            mono.log_warning(mono.DataWarning,
                             ("FITS Headers cannot store a boolean directly "
                              "but can use T/F letters. The boolean has "
                              "been converted."))
            # Convert to a fits proper type.
            converted_value = 'T' if valuedex else 'F'
            ap_fits.setval(filename, keydex, value=converted_value, 
                           comment=comment_cards.get(keydex, None))
        else:
            mono.warn(mono.DataWarning,
                      ("The header card key-value pair ({key} = {value}) "
                       "uses a value type of {value_type}. FITS Headers can "
                       "only use numbers and ASCII strings. Converting it "
                       "to a string."
                       .format(key=keydex, value=str(valuedex), 
                               value_type=type(valuedex))))
            # Convert to a fits proper type.
            converted_value = str(valuedex)

            # If the key, value and comment card entry is too big, 
            # (>=80) it is better to open and write the entire file 
            # for the CONTINUE card.
            card_length = (len(keydex) 
                           + len(str(converted_value)) 
                           + len(str(comment_cards.get(keydex,''))))
            if (card_length >= 80):
                __, hdu_header, hdu_data = read_fits_file(
                    filename=filename, extension=0, silent=True)
                # Change the header.
                hdu_header.set(keydex, converted_value, 
                               comment_cards.get(keydex,None))
                # Finally, over/re-write the file to save the change.
                write_fits_file(filename=filename, 
                                hdu_header=hdu_header, hdu_data=hdu_data, 
                                hdu_object=None,
                                save_file=True, overwrite=True, silent=True)
            else:
                ap_fits.setval(filename, keydex, value=converted_value, 
                               comment=comment_cards.get(keydex,None))
    return None