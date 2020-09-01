
import copy
import secrets
import string

import sparrowmonolith as mono

# Prefixes, suffixes, and infix (or all affix) operations.
##########
def add_prefix(string, prefix):
    """ This function adds a prefix string to the string. This
    really is just a stable version of ''.join([prefix, string]).
    
    Parameters
    ----------
    string : string
        The string that the prefix of which will be taken out.
    prefix : string
        The prefix.

    Returns
    -------
    string : string
        The string, with the new prefix.
    """
    # It is just a wrapper around join.
    return ''.join([prefix, string])

def add_suffix(string, suffix):
    """ This function adds a suffix string to the string. This
    really is just a stable version of ''.join([string, suffix]).
    
    Parameters
    ----------
    string : string
        The string that the suffix of which will be taken out.
    suffix : string
        The suffix.

    Returns
    -------
    string : string
        The string, with the new suffix.
    """
    # It is just a wrapper around join.
    return ''.join([string, suffix])

def delete_prefix(string, prefix):
    """ This function deletes the prefix string of a string. If
    the prefix does not exist, the string is returned unchanged.

    See https://stackoverflow.com/a/16891418

    Parameters
    ----------
    string : string
        The string that the prefix of which will be taken out.
    prefix : string
        The prefix.

    Returns
    -------
    base : string
        The string, without the prefix.

    """
    try:
        # This behavior is available in Python 3.9+. As such, 
        # we have the fall back.
        string.removeprefix(prefix)
    except Exception:
        # The fall back solution.
        if string.startswith(prefix):
            string = string[len(prefix):]
        else:
            string = string
    finally:
        # Return, all done, naming convention.
        base = string
        return base

    # The code should not reach here.
    raise mono.BrokenLogicError
    return None

def delete_suffix(string, suffix):
    """ This function deletes the suffix string of a string. If
    the suffix does not exist, the string is returned unchanged.

    See https://stackoverflow.com/a/16891418

    Parameters
    ----------
    string : string
        The string that the suffix of which will be taken out.
    suffix : string
        The suffix.

    Returns
    -------
    base : string
        The string, without the suffix.

    """
    try:
        # This behavior is available in Python 3.9+. As such, 
        # we have the fall back.
        string.removesuffix(suffix)
    except Exception:
        # The fall back solution.
        if string.endswith(suffix):
            string = string[:-len(suffix)]
        else:
            string = string
    finally:
        # Return, all done, naming convention.
        base = string
        return base

    # The code should not reach here.
    raise mono.BrokenLogicError
    return None

def delete_substrings(string, substrings):
    """ Deletes all occurrences of any substrings provided from the 
    original string.

    Parameters
    ----------
    string : string
        The string to be purged of all substrings.
    substrings : string or list
        The substrings in a list, or a string by itself.

    Returns
    -------
    purged_string : string
        The string after it had all substring occurrences taken out.    
    """
    # Just in case.
    original_string = copy.deepcopy(string)

    # Check if the substring is singular or is a list of substrings. 
    # It is better to handle a one long list.
    if (isinstance(substrings, str)):
        substrings = [substrings,]
    elif (isinstance(substrings, (list, tuple))):
        pass
    else:
        # It must be a string or a list of strings.
        raise mono.InputError("The substring input must be a string or "
                              "list of strings.")
    
    # Purge all substrings using the built-in replace method and 
    # going through.
    for substringdex in substrings:
        original_string = original_string.replace(substringdex, '')

    # Naming convention.
    purged_string = original_string
    return purged_string

# Creating a random string.
##########
def random_string(length, characters=None):
    """ This function returns a random string of characters of 
    some length from a set of characters to use.

    Credit to: https://stackoverflow.com/a/23728630

    Parameters
    ----------
    length : int
        The length of the random string.
    characters : string (optional)
        The total available characters to use. The order does 
        not matter. Use None for default string set: all lowercase
        letters.

    Returns
    -------
    random_string : string
        The random string of proper length.    
    """
    
    # Basic type checking.
    length = int(length)
    # If the characters list is None, just use default string set
    # of all lowercase.
    if (characters is None):
        characters = string.ascii_lowercase
    else:
        characters = str(characters)

    # Implementing the random string generator found from the 
    # credited link.
    random_string = ''.join([secrets.choice(characters) 
                             for __ in range(length)])
    # All done
    return random_string





