from base64 import b64encode
import click
import requests


@click.command()
@click.option('--email', prompt='email')
@click.option('--password', prompt='password', hide_input=True)
def login(email, password):
    click.echo('Attempting login for {}...'.format(email))
    empw = '{0}:{1}'.format(email, password)
    empw_enc = b64encode(empw.encode('utf-8')).decode('utf-8')
    header = 'Basic {0}'.format(empw_enc)
    res = requests.post('https://wholenoteapp.com/api/v1.0/login',
                        headers={'Authorization': header})
    click.echo(res.json())
