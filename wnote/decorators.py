from click import echo
from functools import wraps

from .auth import login_request
from .exceptions import FailedRequestException


def catch_failed_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except FailedRequestException as ex:
            return echo(ex.pretty_message)

    return decorated_function


def access_token_required(f):
    @wraps(f)
    def decorated_function(config, *args, **kwargs):
        email = config.email
        password = config.password
        try:
            access_token = login_request(email, password)
            echo('Login for {0} successful'.format(email))
            return f(config=config, access_token=access_token, *args, **kwargs)
        except FailedRequestException as ex:
            return echo(ex.pretty_message)

    return decorated_function
