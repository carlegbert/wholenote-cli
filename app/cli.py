import click
from app.auth import login_request


@click.command()
@click.option('--email', prompt='email')
@click.option('--password', prompt='password', hide_input=True)
def login(email, password):
    click.echo('Attempting login for {}...'.format(email))
    return login_request(email, password)
