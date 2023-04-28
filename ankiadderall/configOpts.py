import configparser
import sys
import os
import tomli_w
import logging
main_logger = logging.getLogger(__name__)


class parsed_config:

    """class for read config

    Other functions retrieve attributes from this class.

    """

    def __init__(self, argparse=None):

        # get attributes key from argparse without value
        if argparse is not None:
            for k in vars(argparse).keys():
                setattr(self, k, None)

        # overwrite Hard coded config

        self.deck = 'Default'
        self.cardtype = 'Basic'
        self.ip = '127.0.0.1'
        self.port = 8765
        self.IFS = '\t'
        self.column = None
        self.file = None
        self.dryrun = False
        self.verbose = None
        self.debug = None

    # config
    def overwrite_config(self, configparse: dict, section_title=None):
        """
        Overwrites options of a config file with arg parser options
        """

        if section_title is None:
            if configparse is None:
                return
            if not isinstance(configparse, dict):
                configparse = vars(configparse)
            for k, v in configparse.items():
                if v is not None:
                    setattr(self, k, v)

        else:
            for k, v in make_toml(configparse, section_title)[section_title].items():
                if v is not None:
                    setattr(self, k, v)

    config_file_name = os.path.expanduser('~/.asprc') if not config_file_name \
                                                        else os.path.expanduser(config_file_name)

    if section is None:
        section = 'default'

    try:
        with open(config_file_name, "r") as f:
            from tomlkit import loads
            toml_load = loads(f.read())

    # if there is no ~/.asprc nor config_file_name, then return empty dict.
    except:
        return {}

    try:
        return toml_load[section]
    except:
        return {}

def make_toml(parsed_arg: dict, section_title='untitled'):

    if not isinstance(parsed_arg, dict):
        parsed_arg = vars(parsed_arg)

    # if v has any value
    return {section_title : {k: v for k, v in parsed_arg.items()
                           if v is not None and k not in {'cardContents', 'alias', 'config', 'toml_generate',
                                                          'toml_section', 'toml_write'}}}

def toml_arg_handle(Do_print_toml, config_file_name, section_title, parsed_arg):
    if config_file_name or Do_print_toml:
        toml = make_toml(parsed_arg, section_title)
        if Do_print_toml:
            print(tomli_w.dumps(toml))

        if config_file_name:
            with open(config_file_name, "wb") as f:
                tomli_w.dump(toml, f)

        exit(2)
