import click
from os import environ
import requests
from subprocess import call
import tempfile

from .util import send_request


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
        txt = self.text if self.text else '<note text is empty>'
        click.echo(txt)

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
        url = 'https://wholenoteapp.com/api/v1.0/notes/' + self.title_id
        data = {'title': self.title, 'text': self.text}
        res = send_request(access_token, requests.put, url, data)
        return res


def get_notes(access_token, refresh_count=0):
    """Get all notes belonging to a user from server"""
    url = 'https://wholenoteapp.com/api/v1.0/notes'

    payload = send_request(access_token, requests.get, url)
    if payload:
        return [Note(**n) for n in payload['notes']]
    return None


def get_note(access_token, title_id, refresh_count=0):
    """Get Note object from server"""
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id

    payload = send_request(access_token, requests.get, url)
    if payload:
        return Note(**payload)
    return None


def delete_note(access_token, title_id, refresh_count=0):
    """Delete note from server"""
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id
    return send_request(access_token, requests.delete, url)
