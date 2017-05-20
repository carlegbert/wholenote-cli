class FailedRequestException(Exception):
    """Exception raised when a request fails.

    FailedRequestException should contain the error message and the status code
    from the failed request."""

    def __init__(self, status_code, errmsg):
        self.errmsg = errmsg
        self.status_code = status_code
        self.pretty_message = '{0}: {1}'.format(status_code, errmsg)
