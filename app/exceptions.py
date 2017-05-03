class AuthFailException(Exception):
    """Exception raised when an authentication request (or other request
    for protected data) fails. In the future this might be subclassed into
    more specific exceptions.

    AuthFailExceptions should contain the error message and the status code
    from the failed request."""

    def __init__(self, errmsg, status_code):
        self.errmsg = errmsg
        self.status_code = status_code
        self.pretty_message = '{0}: {1}'.format(status_code, errmsg)
