import click
import json
from os import environ
import requests
from subprocess import call
import tempfile

from app.auth import construct_bearer_header, refresh_request


class Note(object):

    def __init__(self, title, titleId, id, text, lastModified, owner):
        self.title = title
        self.title_id = titleId
        self.id = id
        self.text = text
        self.last_modified = lastModified

    def display(self):
        click.echo('title: ' + self.title)
        click.echo('title id: ' + self.title_id)
        click.echo('permanent ID:' + self.id)
        click.echo('-'*20)
        click.echo(self.text)

    def open_in_editor(self):
        """Open file in editor specified by user's environment variable
        (defaults to nano). Returns true if text is changed, false if not.
        """
        ed = environ.get('EDITOR', 'nano')
        with tempfile.NamedTemporaryFile(suffix='.tmp') as f:
            f.write(self.text.encode())
            f.flush()
            call([ed, f.name])
            f.seek(0)
            new_text = f.read().decode('utf-8')
            if new_text != self.text:
                self.text = new_text
                return True
            return False

    def update(self, access_token, refresh_count=0):
        header = construct_bearer_header(access_token)
        url = 'https://wholenoteapp.com/api/v1.0/notes/' + self.title_id
        data = {'title': self.title, 'text': self.text}
        res = requests.put(url, headers=header, json=data)
        res_data = res.json()
        if res.status_code == 200:
            click.echo(self.title_id+' updated succesfully.')
            return res_data
        elif refresh_count > 3:
            click.echo('Error authenticating token. You may need to log in again.')
        elif res.status_code == 422:
            access_token = refresh_request()
            refresh_count += 1
            return self.update(access_token, refresh_count)
        else:
            click.echo('{0}: {1}'.format(res.status_code, res_data['msg']))


def get_notes(access_token, refresh_count=0):
    """Get all notes belonging to a user from server"""
    header = construct_bearer_header(access_token)
    res = requests.get('https://wholenoteapp.com/api/v1.0/notes',
                       headers=header)
    data = res.json()
    if res.status_code == 200:
        return [Note(**n) for n in data['notes']]
        return data['notes']
    elif refresh_count > 3:
        click.echo('Error authenticating token. You may need to log in again.')
    elif res.status_code == 422:
        access_token = refresh_request()
        refresh_count += 1
        return get_notes({access_token: access_token}, refresh_count)
    else:
        click.echo('{0}: {1}'.format(res.status_code, data['msg']))


def note_detail(access_token, title_id, refresh_count=0):
    """Get Note object from server"""
    header = construct_bearer_header(access_token)
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id
    res = requests.get(url, headers=header)
    data = res.json()
    if res.status_code == 200:
        return Note(**data)
    elif refresh_count > 3:
        click.echo('Error authenticating token. You may need to log in again.')
    elif res.status_code == 422:
        access_token = refresh_request()
        refresh_count += 1
        return get_notes({access_token: access_token}, refresh_count)
    else:
        click.echo('{0}: {1}'.format(res.status_code, data['msg']))


def delete_note(access_token, title_id, refresh_count=0):
    """Delete note from server"""
    header = construct_bearer_header(access_token)
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id
    res = requests.delete(url, headers=header)
    data = res.json()
    if res.status_code == 200:
        click.echo('Note {0} deleted.'.format(title_id))
    elif refresh_count > 3:
        click.echo('Error authenticating token. You may need to log in again.')
    elif res.status_code == 422:
        access_token = refresh_request()
        refresh_count += 1
        return get_notes({access_token: access_token}, refresh_count)
    else:
        click.echo('{0}: {1}'.format(res.status_code, data['msg']))
