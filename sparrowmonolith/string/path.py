
"""
These are functions which deal with the manipulation of strings 
which contain path information.
"""

import os

def split_path(path):
    """ This function splits a pathname into the directory, file, 
    and extension names.
    
    Parameters
    ----------
    path : string
        The path that is to be split.

    Returns
    -------
    directory : string
        The directory component of the path.
    file_name : string
        The file name component of the path.
    extension : string
        The extension component of the path.
    """
    # Type checking.
    path = str(path)

    # Split the pathname into directory/filename.extension.
    directory = os.path.split(path)[0]
    file_name = os.path.splitext(os.path.split(path)[1])[0]
    extension = os.path.splitext(path)[1]

    return directory, file_name, extension

def combine_path(directory=None, filename=None, extension=None):
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