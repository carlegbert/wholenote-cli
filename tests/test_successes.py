""" Tests for 'wnote get <title>' """

from wnote.cli import cli


def test_get_all(runner, cfg_opt):
    result = runner.invoke(cli, [cfg_opt, 'get'])
    assert result.exit_code == 0
    assert 'notes retrieved' in result.output


def test_get_single(runner, cfg_opt):
    result = runner.invoke(cli, [cfg_opt, 'get', 'static_test_note'])
    assert result.exit_code == 0
    assert 'static_test_note_text' in result.output


def test_get_create_note(runner, cfg_opt):
    result = runner.invoke(cli, [cfg_opt, 'new', 'new_test_note'])
    assert result.exit_code == 0
    assert 'new_test_note created successfully' in result.output


def test_write_to_note(runner, cfg_opt):
    opts = [cfg_opt, 'write', 'new_test_note', 'new_note_text']
    result = runner.invoke(cli, opts)
    assert result.exit_code == 0
    assert 'updated successfully' in result.output


def test_append_to_note(runner, cfg_opt):
    put_opts = [cfg_opt, 'write', 'new_test_note', '--append', 'appended_text']
    put_result = runner.invoke(cli, put_opts)
    get_opts = [cfg_opt, 'get', 'new_test_note']
    get_result = runner.invoke(cli, get_opts)
    assert put_result.exit_code == 0
    assert get_result.exit_code == 0
    assert 'updated successfully' in put_result.output
    assert 'new_note_text\nappended_text' in get_result.output


def test_prepend_to_note(runner, cfg_opt):
    put_opts = [cfg_opt, 'write', 'new_test_note', '--prepend',
                'prepended_text']
    put_result = runner.invoke(cli, put_opts)
    get_opts = [cfg_opt, 'get', 'new_test_note']
    get_result = runner.invoke(cli, get_opts)
    assert put_result.exit_code == 0
    assert get_result.exit_code == 0
    assert 'updated successfully' in put_result.output
    assert 'prepended_text\nnew_note_text' in get_result.output


def test_update_note_title(runner, cfg_opt):
    result = runner.invoke(cli, [cfg_opt, 'newtitle', 'new_test_note',
                                 'updated_test_title'])
    assert result.exit_code == 0
    assert 'updated_test_title' in result.output


def test_delete_note(runner, cfg_opt):
    result = runner.invoke(cli, [cfg_opt, 'delete', 'updated_test_title'])
    assert result.exit_code == 0
    assert 'updated_test_title' in result.output
