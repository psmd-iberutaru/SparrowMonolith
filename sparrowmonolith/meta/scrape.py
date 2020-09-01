
"""
This houses functions and modules that deal solely with the 
usage and manipulations of pure Python source files, rather than 
Python objects as per normal.
"""

import types
import importlib

import sparrowmonolith as mono

def load_module_file(pathname):
    """ This function loads arbitrary source files as a module 
    object to use.

    Parameters
    ----------
    pathname : string
        The file path to the module file, it can be relative or 
        absolute.

    Returns
    -------
    module : module
        The loaded python file as a module.
    """
    # Break up the file name and the pathname. The pathname is
    # needed to locate the file, the file name itself can be the 
    # "name" of the module.
    __, filename, __ = mono.meta.split_pathname(pathname=pathname)
    # Load the module.
    loader = importlib.machinery.SourceFileLoader(filename, pathname)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    # All done.
    return module

