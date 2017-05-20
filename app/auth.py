from base64 import b64encode
from os import path

import requests
import click

from app.exceptions import FailedRequestException


def construct_basic_header(email, password):
    """Construct b64 encoded header for HTTP Basic auth"""
    empw = '{0}:{1}'.format(email, password)
    empw_enc = b64encode(empw.encode('utf-8')).decode('utf-8')
    return {'Authorization': 'Basic {0}'.format(empw_enc)}


def construct_bearer_header(tkn):
    """Construct header to send access or refresh token to server"""
    return {'Authorization': 'Bearer {0}'.format(tkn)}


def read_refresh_token():
    """Read refresh token from ~/.wnre"""
    p = path.expanduser('~/.wnre')
    try:
        with open(p, 'r') as f:
            tkn = f.readline()
            return tkn
    except FileNotFoundError:
        return None


def read_access_token():
    """Read access token from ~/.wnac"""
    p = path.expanduser('~/.wnac')
    try:
        with open(p, 'r') as f:
            tkn = f.readline()
            return tkn
    except FileNotFoundError:
        return None


def write_refresh_token(rtkn):
    """Read refresh token from ~/.wnre"""
    p = path.expanduser('~/.wnre')
    with open(p, 'w+') as f:
        f.write(rtkn)


def write_access_token(access_token):
    """Read access token from ~/.wnac"""
    p = path.expanduser('~/.wnac')
    with open(p, 'w+') as f:
        f.write(access_token)


def login_request():
    """Send login request and return WholenoteCredentials object on
    success. Raise exception on failure."""
    email = click.prompt('email')
    password = click.prompt('password', hide_input=True)
    click.echo('+'*20)
    header = construct_basic_header(email, password)
    res = requests.post('https://wholenoteapp.com/api/v1.0/login',
                        headers=header)
    data = res.json()
    if res.status_code == 200:
        rtkn = data['refresh_token']
        access_token = data['access_token']
        write_refresh_token(rtkn)
        write_access_token(access_token)
        return access_token
    else:
        raise FailedRequestException(res.status_code, data['msg'])


def refresh_request():
    """Use refresh token to get useable access token."""
    click.echo('Access token timed out... making refresh request')
    rtkn = read_refresh_token()
    header = construct_bearer_header(rtkn)
    res = requests.post('https://wholenoteapp.com/api/v1.0/refresh',
                        headers=header)
    data = res.json()
    if res.status_code == 200:
        access_token = data['access_token']
        write_access_token(access_token)
        return access_token
    else:
        raise FailedRequestException(res.status_code, data['msg'])
