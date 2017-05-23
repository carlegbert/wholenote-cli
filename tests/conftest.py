from os import getcwd, path

from click.testing import CliRunner
import pytest


@pytest.fixture(scope='function')
def runner():
    return CliRunner()


@pytest.fixture(scope='function')
def cfg_opt():
    return '--config-file=' + path.join(getcwd(), 'tests', 'test_config.ini')
