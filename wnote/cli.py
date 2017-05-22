from os import environ, path

import click
from .config import Config
from .decorators import (
        access_token_required,
        catch_failed_request
    )
from .note import (
        get_single_note,
        get_all_notes,
        delete_note,
    )


CFG_FILE = path.join(environ['HOME'], '.config', 'wnote', 'config.ini')


@click.group()
@click.option('--config-file', default=CFG_FILE)
@catch_failed_request
@click.pass_context
def cli(ctx, config_file):
    """entry point"""
    ctx.obj = Config.from_file(config_file)


@click.command()
@click.argument('title', required=False)
@click.pass_obj
@access_token_required
def get(config, access_token, title):
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
@click.pass_obj
@access_token_required
def delete(config, access_token, title):
    delete_note(access_token, title)
    click.echo('Note {} deleted.'.format(title))


@click.command()
@click.argument('title')
@click.option('--write', 'operation_type', flag_value='write', default=True)
@click.option('--append', 'operation_type', flag_value='append')
@click.option('--prepend', 'operation_type', flag_value='prepend')
@click.argument('content')
@click.pass_obj
@access_token_required
def write(config, access_token, title, content, operation_type):
    note = get_single_note(access_token, title)
    old_text = note.text

    if operation_type == 'append':
        note.text += '\n' + content
    elif operation_type == 'prepend':
        note.text = content + '\n' + note.text
    elif operation_type == 'write':
        note.text = content

    if note.text == old_text:
        click.echo('Note not updated (no changes made)')
    elif note.save(access_token):
        click.echo(note.title_id+' updated succesfully.')


@click.command()
@click.argument('title')
@click.pass_obj
@access_token_required
def edit(config, access_token, title):
    note = get_single_note(access_token, title)
    old_text = note.text
    note.open_in_editor(config.editor)
    if note.text == old_text:
        click.echo('Note not updated (no changes made)')
    elif note.save(access_token):
        click.echo(note.title_id+' updated succesfully.')
    note.save(access_token)


cli.add_command(get)
cli.add_command(delete)
cli.add_command(write)
cli.add_command(edit)
