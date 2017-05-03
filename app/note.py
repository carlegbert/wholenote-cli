import click
import requests

from app.auth import (
        construct_bearer_header,
        read_access_token,
        refresh_request
    )


def get_notes(atkn, refresh_count=0):
    """Get all notes belonging to a user"""
    if not atkn:
        atkn = read_access_token()
    header = construct_bearer_header(atkn)
    res = requests.get('https://wholenoteapp.com/api/v1.0/notes',
                       headers=header)
    data = res.json()
    if res.status_code == 200:
        return data['notes']
    elif res.status_code == 422 and refresh_count > 3:
        atkn = refresh_request()
        refresh_count += 1
        return get_notes({atkn: atkn}, refresh_count)
    else:
        click.echo('{0}: {1}'.format(res.status_code, data['error']))
