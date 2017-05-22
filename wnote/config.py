from configparser import ConfigParser
from os import path, environ, makedirs

from click import echo


CFG_DIR = path.join(environ['HOME'], '.config', 'wnote')
CFG_FILE = path.join(CFG_DIR, 'config.ini')
REFRESH_FILE = path.join(CFG_DIR, '.wnrt')


class Config(object):
    """Object containing configuration information, such as access and
    refresh tokens and user configuration options. Configuration options
    from file are store in cfg property."""
    def __init__(self, options):
        self.options = options

    @property
    def email(self):
        return self.options.get('USER', 'email', fallback='')

    @property
    def password(self):
        return self.options.get('USER', 'password', fallback='')

    @classmethod
    def from_file(cls, filepath=CFG_FILE):
        """Load configuration options from CFG_FILE and use them
        to instantiate a Config object. Takes optional filepath
        argument that allows a different configuration file to
        be loaded (for testing)"""
        expfilepath = path.expanduser(filepath)
        if not path.exists(expfilepath):
            echo('No configuration file found at '+expfilepath)
        config_options = ConfigParser()
        config_options.read(expfilepath)
        return Config(config_options)


def create_config_file(directory=CFG_DIR, basename='config.ini'):
    """Create configuration file & directories"""
    if not path.exists(CFG_DIR):
        makedirs(CFG_DIR)
    cfg = ConfigParser()
    cfg.add_section('USER')
    cfg.add_section('GENERAL')
    with open(CFG_FILE, 'w') as f:
        f.write('# Configuration file for wnote.\n')
