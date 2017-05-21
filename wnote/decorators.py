from click import echo
from functools import wraps

from .auth import login_request
from .config import Config
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
            return f(config=config, access_token=access_token, *args, **kwargs)
        except FailedRequestException as ex:
            return echo(ex.pretty_message)

    return decorated_function


def load_config(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        config = Config.from_file()
        return f(config=config, *args, **kwargs)

    return decorated_function
