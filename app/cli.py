import click
from app.auth import access_token_required
from app.note import get_notes, note_detail


@click.group()
def cli():
    """entry point"""
    pass


@click.command()
@access_token_required
def list(access_token):
    notes = get_notes(access_token)
    click.echo('{0} notes retrieved:'.format(len(notes)))
    for n in notes:
        click.echo('  ' + n.title_id)


@click.command()
@click.argument('title')
@access_token_required
def detail(access_token, title):
    note = note_detail(access_token, title)
    note.display()


@click.command()
@click.argument('title')
def delete(title):
    click.echo('<delete note with title "{}">'.format(title))


@click.command()
@click.argument('title')
@click.argument('content')
@click.option('--append', is_flag=True)
@click.option('--prepend', is_flag=True)
def write(title, content, append, prepend):
    if append and prepend:
        click.echo("can't append and prepend")
    elif append:
        click.echo('<append to note>')
    elif prepend:
        click.echo('<prepend to note>')
    else:
        click.echo('<replace contents of single note>')


@click.command()
@click.argument('title')
def edit(title):
    click.echo('<open a note with $EDITOR and save it when that process ends')


cli.add_command(list)
cli.add_command(detail)
cli.add_command(delete)
cli.add_command(write)
cli.add_command(edit)
