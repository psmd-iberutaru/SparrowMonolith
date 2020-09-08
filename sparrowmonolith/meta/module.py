
"""
This houses functions and modules that deal solely with the 
usage and manipulations of pure Python source files, rather than 
Python objects as per normal.
"""

import types
import importlib
import inspect
import types

import sparrowmonolith as mono

def combine_modules(*args, name=None, docstring=None, **kwargs):
    """ This function combines the name-spaces of multiple modules.
    In essence, it is similar to importing many things under a 
    a single module name.

    Parameters
    ----------
    *args : modules
        The modules to be combined. The right most module will
        always overwrite the left most.
    name : string (optional)
        The name of the module to be done, defaults to 'synthesis'.
    docstring : string (optional)
        The docstring of this module, defaults to 
        'synthesis docstring'
    **kwargs : parameters
        There should be no other keyword arguments, will raise 
        if there are.

    Returns
    -------
    combined_module : module
        The combined module.
    """
    # The defaults.
    name = str(name) if (name is not None) else 'synthesis'
    docstring = (str(docstring) if (docstring is not None) 
                 else 'synthesis docstring')

    # There should be no keyword arguments.
    if (len(kwargs) >= 1):
        raise mono.InputError("There should be no keyword arguments for "
                              "the combining of modules.")
    # It should be as simple as combining all of the members of each
    # module into one dictionary.
    combine_module = types.ModuleType(name, doc=docstring)
    for moduledex in args:
        combine_module.__dict__.update(moduledex.__dict__)
    # All done.
    return combine_module

def load_source_file(pathname):
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

def load_module_functions(module):
    """ This function loads the functions from a module and returns
    it as a dictionary, in a way, it is a wrapper around the 
    inspect module.

    Parameters
    ----------
    module : module
        The module to which the functions from will be loaded.

    Returns
    -------
    functions : dictionary
        The dictionary of functions.
    """
    # A wrapper around the inspect module.
    functions = dict(inspect.getmembers(module, inspect.isfunction))
    return functions