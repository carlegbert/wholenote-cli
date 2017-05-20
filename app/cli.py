import click
from .decorators import access_token_required, catch_failed_request
from .note import (
        get_single_note,
        get_all_notes,
        delete_note,
    )


@click.group()
@catch_failed_request
def cli():
    """entry point"""
    pass


@click.command()
@click.argument('title', required=False)
@access_token_required
def get(access_token, title):
    if not title:
        notes = get_all_notes(access_token)
        click.echo('{0} notes retrieved:'.format(len(notes)))
        for n in notes:
            click.echo('  ' + n.title_id)
    else:
        note = get_single_note(access_token, title)
        note.display(access_token)


@click.command()
@click.argument('title')
@access_token_required
def delete(access_token, title):
    delete_note(access_token, title)
    click.echo('Note {} deleted.'.format(title))


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

    note = get_single_note(access_token_required, title)
    old_text = note.text

    if append:
        note.text += '\n' + content
    elif prepend:
        note.text = content + '\n' + note.text
    else:
        note.text = content

    if note.text == old_text:
        click.echo('Note not updated (no changes made)')
    elif note.save(access_token):
        click.echo(note.title_id+' updated succesfully.')


@click.command()
@click.argument('title')
@access_token_required
def edit(access_token, title):
    note = get_single_note(access_token, title)
    note.open_in_editor()
    note.update()


cli.add_command(get)
cli.add_command(delete)
cli.add_command(write)
cli.add_command(edit)
