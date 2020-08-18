"""
This is a Python API for sending emails.
"""

import sendgrid

import sparrowmonolith as mono

def email_sendgrid(from_email, to_email, subject, content, api_key=None):
    """ This function uses SendGrid's API to send an email. There
    is a limit on 100 emails/day.

    Parameters
    ----------
    from_email : string
        The email address from which the email is sent from.
    to_email: string
        The email addresses which the email is sent to.
    subject : string
        The email subject line. It is suggested that this is a 
        concise message.
    content : string
        The content of the email. It may be formatted using HTML.

    Returns
    -------
    None
    
    """
    # Using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python
    
    # Compile the message.
    message = sendgrid.helpers.mail.Mail(
        from_email=from_email, to_emails=to_email,
        subject=subject, html_content=content)

    # Send the message. This is an API key, it can either be 
    # hard coded here or used as an input.
    api_key = api_key
    if (api_key is None):
        raise mono.InputError("The SendGrid API key is not provided.")
    else:
        using_api_key = api_key
    try:
        sg = sendgrid.SendGridAPIClient(using_api_key)
        response = sg.send(message)
        # Test to see if the email was accepted by the server.
        if (response.status_code == 202):
            # It was accepted.
            pass
        else:
            # It was not formally accepted, there is a different 
            # status code.
            mono.warn(mono.APIWarning,
                      ("The email may not have been sent. The HTTP status "
                       "code for this transaction is: {code}"
                       .format(code=response.status_code)))
    except Exception:
        raise

    return None