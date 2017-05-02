import click
from app.auth import login_request


@click.command()
@click.option('--email', prompt='email')
@click.option('--password', prompt='password', hide_input=True)
def login(email, password):
    click.echo('Attempting login for {}...'.format(email))
    return login_request(email, password)


@click.group()
def cli():
    pass


@click.command()
def list():
    click.echo('<list all notes>')


@click.command()
def detail():
    click.echo('<list contents of single note>')


@click.command()
def delete():
    click.echo('<delete single note>')


@click.command()
def append():
    click.echo('<append content to single note>')


@click.command()
def prepend():
    click.echo('<prepend content to single note>')


@click.command()
def write():
    click.echo('<replace contents of single note>')


@click.command()
def edit():
    click.echo('<open a note with $EDITOR and save it when that proccess ends')


cli.add_command(list)
cli.add_command(detail)
cli.add_command(delete)
cli.add_command(append)
cli.add_command(prepend)
cli.add_command(write)
cli.add_command(edit)
