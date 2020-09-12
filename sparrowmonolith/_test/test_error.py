
"""
These are were the functions to test errors, warnings, and logs are
applied.
"""

import pytest

import sparrowmonolith as mono

@pytest.mark.skip(reason="Not implemented.")
def test_error():
    """ This tests the logging of errors (not the raising of them).
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_warn():
    """ This tests the logging of warnings, as this function also
    raises warnings, they are tested here too.
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_log_warn():
    """ This tests the logging of warnings only. The function being
    tested should not display a warning expect in a log.

    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_info():
    """
    This tests the logging of information. As the information can 
    be printed, it should also test this.
    """
    assert False
    return None

@pytest.mark.skip(reason="Not implemented.")
def test_debug():
    """ This tests debugging messages and their prints if desired. 
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_debug_block():
    """ This tests the debugging functions of a whole block of 
    code, or rather, that any block of code will perform as desired.
    """
    assert False
    return None


@pytest.mark.skip(reason="Not implemented.")
def test_silence_specific_warning():
    """ This tests the silencing of specific messages.
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_silence_sparrow_warnings():
    """ This tests the silencing of SparrowMonolith based warnings.
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_silence_nonsparrow_warnings():
    """ This tests the silencing of non-SparrowMonolith based 
    warnings.
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_silence_all_warnings():
    """ This tests the silencing of all warnings.
    """
    assert False
    return None

@pytest.mark.skip(reason="Not implemented.")
def test_silence_info_message():
    """ This tests the silencing of all informational messages.
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_enable_debug():
    """ This tests the enabling of debugging code within this 
    context manager. 
    """
    assert False
    return None
@pytest.mark.skip(reason="Not implemented.")
def test_disable_debug():
    """ This tests the disabling of debugging code within this
    context manager. 
    """
    assert False
    return None

@pytest.mark.skip(reason="Not implemented.")
def test_silence_everything():
    """ This tests the silencing of all errors, messages, and 
    warnings.
    """
    assert False
    return None
