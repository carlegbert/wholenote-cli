#!venv/bin/python

from app.auth import read_refresh_token, WholenoteCredentials
from app.cli import login


if __name__ == '__main__':
    rtkn = read_refresh_token()
    if rtkn:
        creds = WholenoteCredentials(rtkn)
        print('refresh token found')
    else:
        login()
        print('no refresh token found')
