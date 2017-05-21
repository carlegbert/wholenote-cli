from base64 import b64encode
from os import environ, makedirs, path

import requests
import click

from wnote.exceptions import FailedRequestException


WNOTE_LOCAL_DIR = path.join(environ['HOME'], '.local', 'wnote')
REFRESH_TOKEN_LOC = path.join(WNOTE_LOCAL_DIR, 'rtkn')


def construct_basic_header(email, password):
    """Construct b64 encoded header for HTTP Basic auth"""
    empw = '{0}:{1}'.format(email, password)
    empw_enc = b64encode(empw.encode('utf-8')).decode('utf-8')
    return {'Authorization': 'Basic {0}'.format(empw_enc)}


def construct_bearer_header(tkn):
    """Construct header to send access or refresh token to server"""
    return {'Authorization': 'Bearer {0}'.format(tkn)}


def read_refresh_token():
    """Write refresh token to file. FileNotFound exception will be
    thrown if file doesn't exist and should be caught any time this
    function is called."""
    with open(REFRESH_TOKEN_LOC, 'r') as f:
        tkn = f.readline()
        return tkn


def write_refresh_token(refresh_token):
    """Read refresh token from file"""
    if not path.exists(WNOTE_LOCAL_DIR):
        makedirs(WNOTE_LOCAL_DIR)
    with open(REFRESH_TOKEN_LOC, 'w+') as f:
        f.write(refresh_token)


def login_request():
    """Send login request and return WholenoteCredentials object on
    success. Raise exception on failure."""
    email = click.prompt('email')
    password = click.prompt('password', hide_input=True)
    header = construct_basic_header(email, password)
    res = requests.post('https://wholenoteapp.com/api/v1.0/login',
                        headers=header)
    payload = res.json()
    if res.status_code == 200:
        access_token = payload['access_token']
        return access_token
    else:
        raise FailedRequestException(res.status_code, payload['msg'])


def refresh_request():
    """Use refresh token to get useable access token."""
    try:
        refresh_token = read_refresh_token()
    except FileNotFoundError:
        return None

    header = construct_bearer_header(refresh_token)
    res = requests.post('https://wholenoteapp.com/api/v1.0/refresh',
                        headers=header)
    payload = res.json()
    if res.status_code == 200:
        return payload['access_token']
    else:
        raise FailedRequestException(res.status_code, payload['msg'])
