""" Tests for 'wnote get <title>' """

from wnote.cli import cli


def test_get_all(runner, cfg_opt):
    result = runner.invoke(cli, [cfg_opt, 'get'])
    assert result.exit_code == 0
    assert 'notes retrieved' in result.output
