
"""
This is a Python API for sending emails.
"""

import pytest

import sparrowmonolith as mono

@pytest.mark.skip(reason="Not implemented.")
def test_email_sendgrid(from_email, to_email, subject, content, api_key=None):
    """ This tests the sending of an email from the Sendgrid 
    service. 
    """
    assert False
    return None