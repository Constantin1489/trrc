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

    def __init__(self, configparser=None):
        """Hard coded config"""


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

        if configparser:
            if not isinstance(configparser, dict):
                configparser = vars(configparser)
            for k, v in configparser.items():
                setattr(self, k, v)

    def overwrite_config(self, configparse: dict, section_title):
        """
        Overwrites options of a config file with arg parser options
        """

        for k, v in make_toml(configparse, section_title)[section_title].items():
            setattr(self, k, v)

    def overwrite_w_argparse_set(self, argparse):
        if configparser:
            if not isinstance(argparse, dict):
                argparse = vars(argparse)
            for k, v in argparse.items():
                setattr(self, k, v)

def read_toml_config(config_file_name, section='default'):
    if config_file_name is None:
        return


    config_file_name = '~/.asprc' if not config_file_name else config_file_name

    try:
        with open(config_file_name, "r") as f:
            from tomlkit import loads
            toml_load = loads(f.read())

    except:
        return parsed_config()

    return parsed_config(toml_load[section])

def make_toml(parsed_arg: dict, section_title='untitled'):

    if not isinstance(parsed_arg, dict):
        parsed_arg = vars(parsed_arg)

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
