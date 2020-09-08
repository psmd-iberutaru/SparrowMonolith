
"""
This is a central repository of error classes that may be used.
Warning classes are also used here and can be used similarly.
If the built-in errors suffice, then it would be better to use
those rather than using these here.
"""

import copy
import contextlib
import logging
import warnings

# The base classes for all errors under this module.
class SparrowBaseException(BaseException):
    pass
class SparrowExecption(Exception):
    pass

#####################################################################
#####################################################################
# Errors
#####################################################################
#####################################################################

class AmbiguousError(SparrowExecption):
    """
    This error is normally used when the program cannot figure out
    the intentions of the user. SparrowMonolith generally will not 
    try and predict what the user wants, and will instead fail.
    """

class ConfigurationError(SparrowExecption):
    """
    This error is normally encountered when there are problems with 
    configuration processing (usually because the configuration 
    class is incorrect).
    """
    
class DataError(SparrowExecption):
    """
    This error is used when there is an issue with the fundamental 
    data that this program or module cannot fix. The user should be 
    able to figure out what is the problem.
    """

class FileError(SparrowExecption):
    """ 
    This is a warning to be used when there are issues with file
    reading or writing, or any real warning that would deal with
    file manipulation.
    """
    pass

class IllogicalProsedureError(SparrowExecption):
    """
    This error is thrown when the program would attempt something 
    that does not make scene. This is usually due to issues with 
    configuration errors.
    """

class ImprecisionError(SparrowExecption):
    """
    This error is used when there are critical issues with numerical 
    precision because of the volume of data or the very low/high 
    numbers involved. It is also just used when data may be chaotic.   
    """
    pass

class InputError(SparrowExecption):
    """
    This error is used when the user does not input a proper or 
    logical entry. 
    """
    pass

class MaskingError(SparrowExecption):
    """
    This error is used when a mask cannot be applied or where there 
    are fatal issues with calculating the mask.
    """
    pass

class MagicError(SparrowExecption):
    """
    This error is used when any routine would utilize 
    magic/hard-coded values for the purposes of any process where 
    said numbers are magic. This is mostly as a programming warning 
    to the user that behavior with magic numbers may not always be 
    expected or logical. This error form is used for higher warning 
    levels, and if the user wants an interrupt when upgrading.
    """

class ModelingError(SparrowExecption):
    """
    This error is used when there are issues with applying or 
    fitting models to a particular set of data. May be used 
    hand-in-hand with DataError.
    """

########################  TERMINAL Errors  ########################
# The common way for formatting TERMINAL error strings.
def _common_terminal_string_format(message):
    # The capital TERMINAL letters.
    terminal_prefix = 'TERMINAL:'

    # The original message.
    if (isinstance(message, str)):
        original_message = message
    else: 
        # It is not a valid type.
        raise TypeError("The message for a TERMINAL error must be a "
                         "string type.")
        # If the message gets here, something really is wrong.
        raise TerminalError("The message for a TERMINAL error must be a "
                            "string type. The previous TypeError was not "
                            "properly raised.")

    # The extra information regarding who to contact and how
    # to "fix it".
    contact_suffix = ("\n >> Please contact project maintainers or "
                      "Sparrow to resolve this issue. ")
    
    # The finished message. The spaces are for spacing.
    formatted_message = '  '.join(
        [terminal_prefix, original_message, contact_suffix])
    return formatted_message

class AssumptionError(SparrowBaseException):
    """
    This error is reserved for instances where something 
    unexpected has occurred because of a flaw in the understanding 
    of assumptions about Python or module functions. 
    """
    def __init__(self, message=None):
        # See if the user's message or a default message should be
        # applied.
        if (isinstance(message, str)):
            # The user's message.
            user_message = message
        else:
            # A default message.
            user_message = ("An erroneous result has transpired because of "
                            "an incorrect assumption about how Python or "
                            "other Python modules or functions work.")
        # Format either message regardless.
        self.message = _common_terminal_string_format(message=user_message)

    def __str__(self):
        return self.message

    pass

class BrokenLogicError(SparrowBaseException):
    """
    This error is encountered when the program enters in a place it 
    should not be able to. Incorporated mostly for safety; usually 
    not the fault of the user. 
    """
    def __init__(self, message=None):
        # See if the user's message or a default message should be
        # applied.
        if (isinstance(message, str)):
            # The user's message.
            user_message = message
        else:
            # A default message.
            user_message = ("Something is not right with the code's logic. "
                            "It has arrived to a place considered "
                            "impossible from the logic flow.")
        # Format either message regardless.
        self.message = _common_terminal_string_format(message=user_message)

    def __str__(self):
        return self.message

    pass

class DeprecatedError(SparrowBaseException):
    """
    This is used when the code should be using a different 
    equivalent function. This is mostly used for cases where a 
    warning has already been issued, or to clean up the core 
    sections of the code during testing. 
    """
    def __init__(self, message=None):
        # See if the user's message or a default message should be
        # applied.
        if (isinstance(message, str)):
            # The user's message.
            user_message = message
        else:
            # A default message.
            user_message = ("This function is terminally deprecated. There "
                            "exists a different and equivalent function. "
                            "Use that function instead.")
        # Format either message regardless.
        self.message = _common_terminal_string_format(message=user_message)

    def __str__(self):
        return self.message

    pass

class DevelopmentError(SparrowBaseException):
    """
    This is used when the code is improperly written as a result of
    development solely by one or many parties. An error here usually
    is because some assumptions on development has been imposed that
    may have been forgotten about.
    """
    def __init__(self, message=None):
        # See if the user's message or a default message should be
        # applied.
        if (isinstance(message, str)):
            # The user's message.
            user_message = message
        else:
            # A default message.
            user_message = ("There seems to be an error in the "
                            "development of this code script or library.")
        # Format either message regardless.
        self.message = _common_terminal_string_format(message=user_message)

    def __str__(self):
        return self.message

class IncompleteError(SparrowBaseException):
    """
    This used when the code is trying to use a function that is 
    incomplete or not usable. This should mostly only be used as 
    a backup or more advanced version of a NotImplementedError 
    (that is, used for cases where implementation is not to be done
    for a few versions for various reasons).
    """
    def __init__(self, message=None):
        # See if the user's message or a default message should be
        # applied.
        if (isinstance(message, str)):
            # The user's message.
            user_message = message
        else:
            # A default message.
            user_message = ("This section of the code is incomplete "
                            "and likely does not work at all. Proceeding "
                            "is not allowed.")
        # Format either message regardless.
        self.message = _common_terminal_string_format(message=user_message)

    def __str__(self):
        return self.message

class TerminalError(SparrowBaseException):
    """
    This is used when something has gone terribly wrong. It is best 
    to contact the maintainers or Sparrow. 
    """
    def __init__(self, message=None):
        # See if the user's message or a default message should be
        # applied.
        if (isinstance(message, str)):
            # The user's message.
            user_message = message
        else:
            # A default message.
            user_message = ("A general TERMINAL error has been raised.")
        # Format either message regardless.
        self.message = _common_terminal_string_format(message=user_message)

    def __str__(self):
        return self.message



#####################################################################
#####################################################################
# Warnings and other Non-Exceptions
#####################################################################
#####################################################################

# The base of all warnings.
class SparrowWarning(UserWarning):
    pass


class AmbiguousWarning(SparrowWarning):
    """
    This warning is normally used when the program cannot figure out
    the intentions of the user. It is not enough confusion to 
    warrant a fail and will instead return the ambiguous results.
    """

class APIWarning(SparrowWarning):
    """
    This warning is to be used when there is an issue with the
    operation of an API.
    """


class ConfigurationWarning(SparrowWarning):
    """
    This warning is used when there are issues with the 
    configuration class and that data is missing. However, the 
    missing data does not warrant an exception.
    """

class DataWarning(SparrowWarning):
    """
    This warning is used when there is an issue with the fundamental 
    data that this program or module cannot fix but can still work 
    around. The user should be able to figure out what is the problem.
    """

class DeprecatedWarning(SparrowWarning):
    """
    This warning is used when there are some functions that are 
    used but have since been replaced with better functions, or 
    where the previous function is not very stable or integrated 
    with the rest of the functions.
    """
    pass

class ErrorWarning(SparrowWarning):
    """
    This warning is to inform that there was an error that was 
    thrown as a warning (either as a critical warning log or 
    something else.
    """

class FileWarning(SparrowWarning):
    """ 
    This is a warning to be used when there are issues with file
    reading or writing, or any real warning that would deal with
    file manipulation.
    """
    pass

class ImprecisionWarning(SparrowWarning):
    """
    This warning is used when there may be issues with numerical 
    precision because of the volume of data or the very low/high 
    numbers involved. 
    """
    pass

class InputWarning(SparrowWarning):
    """
    This warning is used when the user inputs something that is 
    questionable, but not wrong.
    """
    pass

class MagicWarning(SparrowWarning):
    """
    This warning is used when any routine would utilize 
    magic/hard-coded values for the purposes of any process where 
    said numbers are magic. This is mostly as a programming 
    warning to the user that behavior with magic numbers may not 
    always be expected or logical.
    """

class MaskingWarning(SparrowWarning):
    """
    This warning is used when any masking or filtering routine 
    (especially in the masking and filtering scripts) fails to 
    mask any pixels or something else is amiss. It is not a bad 
    thing, but it can be helpful to know. 
    """
    pass

class MemoryWarning(SparrowWarning):
    """
    This warning is used to warn the user that the procedures that 
    follow would require a lot of memory RAM. If instead it would 
    produce a large file(s), StorageWarning should be used.
    """
    pass

class OverwriteWarning(SparrowWarning):
    """
    This warning is used to warn the user that a file has been 
    overwritten, most likely because of conflicting file names.
    """
    pass

class ReductionWarning(SparrowWarning):
    """
    This warning is used when normally unusual parameters are 
    used for data reduction. The user is trusted in their procedures.
    """
    pass

class StorageWarning(SparrowWarning):
    """
    This warning is used when the large file(s) would be written 
    to the hard drive. If instead a lot of RAM would be used, it is 
    better to use MemoryWarning.
    """

class TimeWarning(SparrowWarning):
    """
    This warning is used when any method called may take a long time 
    to compute or execute. This allows the user to stop and change 
    if desired. 
    """
    pass


####################################################################
####################################################################
# Non-raise Error, Warning, Informational, and Logging Messages
####################################################################
####################################################################

def error(type, message):
    """ This is a wrapper around the logging's error command. 
    However, it does not raise an error. Instead, an error may be 
    sent to and it will be converted into a proper warning.

    Parameters
    ----------
    type : ExecptionsClass
        The error that could be raised, but it is more manageable as 
        a logged error.
    message : string
        The message that the error is to give.

    Returns
    -------
    None
    """
    # Ensure that the type really is an error.
    if (not issubclass(type, Exception)):
        raise AssumptionError("It is assumed that logging errors should "
                              "be raise-able. This type class is not a "
                              "raise-able exception.")
    try:
        error_name = str(type.__name__)
    except Exception:
        # Or just apply a default.
        error_name = 'UserError'
    except (BaseException, SparrowBaseException):
        # Unless they are major errors, then re-raise them.
        raise 
    finally:
        error_message = ''.join(['[', error_name, ']', '  ', message])
    # Log the error.
    logging.error(error_message)
    # ...and inform.
    warnings.warn(error_message, ErrorWarning, stacklevel=2)
    return None

def warn(type, message):
    """ Just a wrapper function around the warning's warn command.

    This wrapper was really only for the logical flow of Sparrow.

    Parameters
    ----------
    type : Warnings Class
        The warning class type.
    message : string
        The message that the warning is to give to the user.

    Returns
    -------
    None
    """
    warnings.warn(message, type, stacklevel=2)
    # Also add it into the logger, but, add information to 
    # indicate that is was a raised warning.
    log_warn(type=type, message=message)
    return None
    
def log_warn(type, message):
    """ Just a wrapper function around logging's built-in warn. 
    This is to only log a warning but not to display it as a 
    standard warning.

    Parameters
    ----------
    type : Warnings Class
        The warning class type.
    message : string
        The message that the warning is to give to the user.
    """
    try:
        warning_name = str(type.__name__)
    except Exception:
        warning_name = 'UserWarning'
    finally:
        warning_message = ''.join(['[', warning_name, ']', '  ', message])
    # Log the warning.
    logging.warning(warning_message)
    # All done.
    return None

def info(message, print=None):
    """
    This is a wrapper function to print helpful information.
   
    Printing information as the function(s) go on is very helpful. 
    However, using the normal print function doesn't allow for some 
    level of customization and ease of handling. Hence, function 
    for uniformity.

    Parameters
    ----------
    message : string
        The informational message that is to be printed. 
    print : boolean (optional)
        This ensures that the info message is always printed 
        regardless of the logging level set by the logging utility.

    Returns
    -------
    nothing
    """
    # For naming convention.
    console_print = print
    # Use the default console print parameter if not specified.
    if (console_print is not None):
        console_print = bool(console_print)
    else:
        console_print = False
    
    # Test if info messages should not be printed given their
    if (info._silent):
        # Messages should not be printed in general.
        pass
    else:
        # Just a little white space so it is not so cluttered.
        logging.info(''.join(['  ', message]))
        if (console_print):
            print("Info:  " + message)
    return None

# This is the default and will set the silent mode parameter for 
# informational printing, but it ensures not to override anything 
# that may already exist.
if (hasattr(info, '_silent')):
    pass
else:
    info._silent = False

# The message form of the debug information. 
def debug(message, console_print=False):
    """ This is a wrapper function for the printing of debug messages. 

    Given the nature of debug messages, it should be clear that it 
    is a debug message, and should also have the proper silencing 
    capabilities.

    Parameters
    ----------
    message : string
        The message that is to be sent as the debug message.
    console_print : boolean (optional)
        This ensures that the info message is always printed 
        regardless of the logging level set by the logging utility. 
        Default is False.
    
    Returns
    -------
    nothing    
    """
    # Test if info messages should not be printed given their
    if (debug._silent):
        # Messages should not be printed in general.
        pass
    else:
        logging.debug(''.join(['  ', message]))
        if (console_print):
            print("SPARROW-MONO Debug:  " + message)
    return None
# This is the default and will set the silent mode parameter for 
# debug printing, but it ensures not to override anything that may 
# already exist.
if (hasattr(debug, '_silent')):
    pass
else:
    debug._silent = True

@contextlib.contextmanager
def debug_block():
    """ This is a wrapper function for encasing debugging code. 

    The execution of code within a debug block is used to contain 
    easily printed debug information. Debug messages should use the 
    debug function :func:`debug`
    """

    if (debug_block._silent):
        return None
    else:
        yield
    return None
# This is the default and will set the silent mode parameter for debug
# printing, but it ensures not to override anything that may already 
# exist.
if (hasattr(debug_block, '_silent')):
    pass
else:
    debug_block._silent = True


####################################################################
####################################################################
# Enabling/Silencing Context Managers
####################################################################
####################################################################

# To silence a specific type of warning. This is a wrapper function.
@contextlib.contextmanager
def silence_specific_warning(warning_type):
    """ This context manager silences all warnings of a given type. 
    Depending on what was inputed.
    
    Parameters
    ----------
    silenced_warning_type : WarningType
        The warning that should be silenced.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=warning_type)
        yield

    return None

# To silence Sparrow based warnings
@contextlib.contextmanager
def silence_sparrow_warnings():
    """ This context manager silences all Sparrow based warnings, 
    all other warnings are still valid.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=SparrowWarning)
        yield

    return None

# To silence non-SparrowMonolith based warnings
@contextlib.contextmanager
def silence_nonsparrow_warnings():
    """ This context manager silences all non-Sparrow based warnings, 
    all other warnings are still valid.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        warnings.simplefilter("default", category=SparrowWarning)
        yield

    return None

# To silence all warnings
@contextlib.contextmanager
def silence_all_warnings():
    """ This context manager silences all warnings. Warnings should 
    not be printed.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield

    return None

# To silence all informational messages.
@contextlib.contextmanager
def silence_info_message():
    """ This context manager silences all informational messages 
    that may be printed.
    """
    # Store previous state.
    previous_state = copy.deepcopy(info._silent)

    # Trigger silent mode.
    info._silent = True

    yield

    # Release silent mode, return to default.
    info._silent = copy.deepcopy(previous_state)
    return None

# To enable debug messages.
@contextlib.contextmanager
def enable_debug():
    """ This context manager turns all debug messages on for the 
    duration of the context. 
    """
    # Store previous state.
    block_previous_state = copy.deepcopy(debug_block._silent)
    message_previous_state = copy.deepcopy(debug._silent)

    # Turn on debugging (releasing from silence)
    debug_block._silent = False
    debug._silent = False

    yield
    
    # Release to previous state.
    debug_block._silent = copy.deepcopy(block_previous_state)
    debug._silent = copy.deepcopy(message_previous_state)

    return None

# To disable debug messages.
@contextlib.contextmanager
def disable_debug():
    """ This context manager turns all debug messages off for the 
    duration of the context. Given that debug messages are generally 
    off in the first place, usage may be rare.
    """
    # Store previous state.
    block_previous_state = copy.deepcopy(debug_block._silent)
    message_previous_state = copy.deepcopy(debug._silent)

    # Disable by silencing. 
    debug_block._silent = True
    debug._silent = True

    yield
    
    # Release to previous state.
    debug_block._silent = copy.deepcopy(block_previous_state)
    debug._silent = copy.deepcopy(message_previous_state)

    return None

# To silence everything, warnings, informational, and debug messages.
@contextlib.contextmanager
def silence_everything():
    """This context manager silences any and all messages, it 
    basically is a wrapper around all other general context 
    managers (even if there is some overlap).
    """
    with silence_sparrow_warnings(), \
         silence_all_warnings(),  \
         silence_info_message(),  \
         disable_debug():
            yield 

    return None