
"""
This module contains functions that find the pathnames for
files, modules, and other goodies.
"""

import inspect
import os
import glob

import sparrowmonolith as mono



# Functions to deal with paths.
def combine_pathname(directory=None, filename=None, extension=None):
    """ This is the opposite of splitting path names. 

    Parameters
    ----------
    directory : string or list (optional)
        This is the directory component that the path should be 
        attached to. If it is a list, the directory components are
        strung together in order.
    filename : string or list (optional)
        This is the filename component that the path should be 
        attached to. If it is a list, the filename components are
        strung together in order.
    extension : string or list (optional)
        This is the extension component that the path should be 
        attached to. If it is a list, the extension components are
        strung together in order.
    
    Returns
    -------
    pathname : string
        The pathname that is created by combining the parts above.
    """
    # Combine the directories...
    directory = directory if directory is not None else ''
    directory = (directory if isinstance(directory, (list,tuple))
                 else [str(directory)])
    all_directory = os.path.join(*directory)
    # ...the file names...
    filename = filename if filename is not None else ''
    filename = (filename if isinstance(filename, (list,tuple))
                 else [filename])
    all_filename = ''.join(filename)
    # ...and the file extensions.
    extension = extension if extension is not None else ''
    extension = (extension if isinstance(extension, (list,tuple))
                 else [extension])
    all_extension = ''.join(extension)
    # Finally combine all of it into one part.
    pathname = os.path.join(all_directory, 
                            ''.join([all_filename, all_extension]))
    # All done.
    return pathname

def split_pathname(pathname):
    """ This function splits a pathname into the directory, file, 
    and extension names.
    
    Parameters
    ----------
    pathname : string
        The pathname that is to be split.

    Returns
    -------
    directory : string
        The directory component of the pathname.
    file_name : string
        The file name component of the pathname.
    extension : string
        The extension component of the pathname.
    """
    # Type checking.
    pathname = str(pathname)

    # Split the pathname into directory/filename.extension.
    directory = os.path.split(pathname)[0]
    file_name = os.path.splitext(os.path.split(pathname)[1])[0]
    extension = os.path.splitext(pathname)[1]

    return directory, file_name, extension


# Functions to deal with modules.
def get_module_file(module):
    """ This gets the absolute pathname of a module's .py file.
    If the entry is not a module, an error is raised.

    Credit: https://stackoverflow.com/a/12154601

    Parameters
    ----------
    module : module
        The module that its file's pathname will be found.

    Returns
    -------
    pathname : string
        The pathname of the module file, as defined by the 
        operating system.
    """
    # Make sure it is module.
    if (not inspect.ismodule(module)):
        raise mono.InputError("The inputed object is not a module. Its "
                              "type is: `{ty}`"
                              .format(ty=type(module)))
    else:
         # Naming convention.
         pathname = inspect.getfile(module)
         return pathname
    # The code should not reach here.
    raise mono.BrokenLogicError
    return None

def get_module_directory(module):
    """ This gets the absolute directory path of a module's .py 
    file. If the entry is not a module, an error is raised.

    Credit: https://stackoverflow.com/a/12154601

    Parameters
    ----------
    module : module
        The module that its file's pathname will be found.

    Returns
    -------
    directory : string
        The absolute directory of the module file, as defined by the 
        operating system.
    """
    # Make sure it is module.
    if (not inspect.ismodule(module)):
        raise mono.InputError("The inputed object is not a module. Its "
                              "type is: `{ty}`"
                              .format(ty=type(module)))
    else:
         # Naming convention.
         directory = os.path.dirname(inspect.getfile(module))
         return directory
    # The code should not reach here.
    raise mono.BrokenLogicError
    return None


# Functions to deal with files.
def find_file_in_directory(directory, filename, throw=False):
    """ Conducts a simple search text of a directory to find a file 
    within it. If more than one match is found, a warning or error 
    is raised as the result could be ambiguous. 

    Parameters
    ----------
    directory : string
        The directory that should be searched for the file.
    filename : string
        The name of the file that will be searched for.
    throw : boolean
        If True, then if there is a file conflict, an exception 
        will be raised.
    
    Returns
    -------
    file_path : string
        The pathname of the file that was found. If 0, return [],
        if 2+ raise.
    """

    # Obtain all of the files from within that directory.
    search_string = combine_pathname(directory=['**', directory, '**'], 
                                 filename=['*', filename, '*'])
    results = glob.glob(search_string, recursive=True)
    len_results = len(results)
    # Test to see if there is only one result, if not, raise. 
    if (len_results == 0):
        # Bummers, no files found.
        mono.warn("No files found matching the search string: {s_str}"
                  .format(s_str=search_string))
        return results
    elif (len_results == 1):
        # Found a file, return its entire path.
        return results[0]
    elif (len_results >= 2):
        # Warn or throw.
        if (throw):
            raise mono.AmbiguousError("There are more than one matching "
                                      "files: {files}"
                                      .format(files=list(results)))
        else:
            mono.warn(mono.AmbiguousWarning,
                      ("There are more than one matching files: {files}. "
                       "Returning all matching files in a list."
                       .format(files=list(results))))
            return results
    else:
        # The code should not reach here.
        raise mono.BrokenLogicError
    # Or here...
    raise mono.BrokenLogicError
    return None

