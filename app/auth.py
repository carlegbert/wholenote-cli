from base64 import b64encode
from os import path
from app.exceptions import AuthFailException

import requests


class WholenoteCredentials(object):
    """Class encapsulating authentication information"""

    def __init__(self, refresh_token, access_token=None, email=None):
        self.refresh_token = refresh_token
        if not access_token:
            self.get_access_token()

    def get_access_token(self):
        """Send refresh request to server and retrieve access token"""
        header = construct_bearer_header(self.refresh_token)
        res = requests.post('https://wholenoteapp.com/api/v1.0/refresh',
                            headers=header)
        data = res.json()
        print(data)
        self.access_token = data['access_token']


def construct_basic_header(email, password):
    """Construct b64 encoded header for HTTP Basic auth"""
    empw = '{0}:{1}'.format(email, password)
    empw_enc = b64encode(empw.encode('utf-8')).decode('utf-8')
    return {'Authorization': 'Basic {0}'.format(empw_enc)}


def construct_bearer_header(tkn):
    """Construct header to send access or refresh token to server"""
    return {'Authorization': 'Bearer {0}'.format(tkn)}


def read_refresh_token():
    """Read refresh token from ~/.wncli. Later I will change where the token is
    stored..."""
    p = path.expanduser('~/.wncli')
    try:
        with open(p, 'r') as f:
            tkn = f.readline()
            return tkn
    except FileNotFoundError:
        return None


def write_refresh_token(rtkn):
    """Read refresh token from ~/.wncli. Later I will change where the token is
    stored..."""
    p = path.expanduser('~/.wncli')
    with open(p, 'w+') as f:
        f.write(rtkn)


def login_request(email, password):
    """Send login request and return WholenoteCredentials object on success.
    Raise exceptions on failure."""
    header = construct_basic_header(email, password)
    res = requests.post('https://wholenoteapp.com/api/v1.0/login',
                        headers=header)
    data = res.json()
    if res.status_code == 200:
        rtkn = data['refresh_token']
        atkn = data['access_token']
        write_refresh_token(rtkn)
        return WholenoteCredentials(rtkn, atkn, email)
    else:
        err = data['error']
        status_code = res.status_code
        raise AuthFailException(err, status_code)
        # raise exception
        return
