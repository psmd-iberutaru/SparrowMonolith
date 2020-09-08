
"""
These are global tests that affect the entire SparrowMonolith code
base.
"""

import glob
import inspect

import sparrowmonolith as mono

def test_pass():
    """ This is a test that should always pass.
    """

    assert True
    return None

def test_existence():
    """ This test scrapes SparrowMonolith and tests to see if
    every function has an associated test. That is, if the tests 
   for functions exist in the first place. If not, this test fails.
    """
    # Obtain the module directory that this package is in.
    smono_dir = mono.meta.get_module_directory(module=mono)
    # And obtain all of the python files within it.
    smono_files = glob.glob(mono.meta.combine_pathname(
        directory=[smono_dir, '**'], filename=['*'], extension='.py'), 
                            recursive=True)
    # There is no testing to be done for __init__ files.
    smono_files[:] = [fdex for fdex in smono_files 
                      if ('__init__' not in fdex)]
    # Load them as modules and combine them.
    smono_modules = [mono.meta.load_source_file(pathname=fdex) 
                     for fdex in smono_files]
    smono_synthesis = mono.meta.combine_modules(*smono_modules)
    # Find all of the functions within this module.
    smono_functions = mono.meta.load_module_functions(module=smono_synthesis)
    smono_function_names = list(smono_functions.keys())
    # Internal functions do not need to be tested, notated by 
    # prefix '_'.
    smono_function_names = [fndex for fndex in smono_function_names 
                            if (fndex[0] != '_')]
    # Test to see if all of the functions have an associated test
    # function. Only do the compute functions, there is not need
    # for the test functions to be tested.
    smono_compute_functs = [fndex for fndex in smono_function_names 
                            if ('test_' not in fndex)]
    smono_test_functs = [fndex for fndex in smono_function_names 
                            if ('test_' in fndex)]
    for functiondex in smono_compute_functs:
        # Expected test function name.
        expected_text_function = ''.join(['test_', functiondex])
        # Test to see if the test function exists.
        assert_message = ("There does not exist the test function `{t_fn}` "
                          "associated with the computational function "
                          "`{c_fn}`."
                          .format(t_fn=expected_text_function, 
                                  c_fn=functiondex))
        assert expected_text_function in smono_test_functs, assert_message

    # All done.
    return True
