import click
from app.auth import access_token_required
from app.note import (
        get_note,
        get_notes,
        delete_note,
    )


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
    note = get_note(access_token, title)
    note.display()


@click.command()
@click.argument('title')
@access_token_required
def delete(access_token, title):
    delete_note(access_token, title)


@click.command()
@click.argument('title')
@click.option('--append', is_flag=True)
@click.option('--prepend', is_flag=True)
@click.argument('content')
@access_token_required
def write(access_token, title, content, append, prepend):
    if append and prepend:
        click.echo("can't append and prepend")
        return

    note = get_note(access_token, title)
    old_text = note.text

    if append:
        note.text += '\n' + content
    elif prepend:
        note.text = content + '\n' + note.text
    else:
        note.text = content

    if note.text != old_text:
        note.update(access_token)
        click.echo('Note updated')
    else:
        click.echo('Note not updated (no changes made)')


@click.command()
@click.argument('title')
@access_token_required
def edit(access_token, title):
    note = get_note(access_token, title)
    edited = note.open_in_editor()
    if edited:
        note.update(access_token)


cli.add_command(list)
cli.add_command(detail)
cli.add_command(delete)
cli.add_command(write)
cli.add_command(edit)
