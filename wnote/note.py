from click import echo
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

    def display(self, verbose=False):
        if verbose:
            echo('title: ' + self.title)
            echo('title id: ' + self.title_id)
            echo('permanent ID:' + self.id)
            echo('-'*20)
        echo(self.text)

    def open_in_editor(self, editor=None):
        """Open file in editor specified by user's environment variable
        (defaults to nano). Returns true if text is changed, false if not.
        """
        if not editor:
            editor = environ.get('EDITOR', 'nano')
        with tempfile.NamedTemporaryFile(suffix='.tmp') as f:
            f.write(self.text.encode())
            f.flush()
            call([editor, f.name])
            f.seek(0)
            new_text = f.read().decode('utf-8')

        if new_text != self.text:
            self.text = new_text
            return True
        return False

    def save(self, access_token):
        url = 'https://wholenoteapp.com/api/v1.0/notes/' + self.title_id
        data = {'title': self.title, 'text': self.text}
        return send_request(access_token, requests.put, url, data)


def get_all_notes(access_token):
    """Get all notes belonging to a user from server"""
    url = 'https://wholenoteapp.com/api/v1.0/notes'

    payload = send_request(access_token, requests.get, url)
    if payload:
        return [Note(**n) for n in payload['notes']]
    return None


def get_single_note(access_token, title_id):
    """Get Note object from server"""
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id

    payload = send_request(access_token, requests.get, url)
    if payload:
        return Note(**payload)
    return None


def delete_note(access_token, title_id):
    """Delete note from server"""
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id
    return send_request(access_token, requests.delete, url)


def create_note(access_token, title):
    url = 'https://wholenoteapp.com/api/v1.0/notes'
    data = {'title': title, 'text': ''}
    payload = send_request(access_token, requests.post, url, data)
    if payload:
        return Note(**payload['note'])
    return None


def update_title(access_token, title_id, new_title):
    url = 'https://wholenoteapp.com/api/v1.0/notes/' + title_id
    data = {'title': new_title}
    payload = send_request(access_token, requests.put, url, data)
    if payload:
        return Note(**payload['note'])
    return None
