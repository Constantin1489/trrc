import sys
import os
import logging
from tomlkit import loads, exceptions
import tomli_w
main_logger = logging.getLogger(__name__)


class ParsedConfig:

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
        self.ifs = '\t'
        self.field = 'Front:Back:tags'
        self.file = None
        self.dryrun = False
        self.verbose = None
        self.debug = None

    def overwrite_config(self, configparse: dict, section_title=None):
        """
        Overwrites options of a config file with arg parser options
        """

        if section_title is None:
            main_logger.debug('section_title: %s', section_title)

            if configparse is None:
                # this doesn't affect existing attributes
                main_logger.debug('No configs')
                return

            # if configparse is a parser object, then make it a dict
            if not isinstance(configparse, dict):
                configparse = vars(configparse)

            main_logger.debug('configparse: %s', mask_apikey(configparse))

            for key, value in configparse.items():
                if value is not None and value is not False:
                    setattr(self, key, value)
            main_logger.debug('section_title: %s', section_title)

        else:
            for key, value in make_toml(configparse, section_title)[section_title].items():
                if value is not None:
                    setattr(self, key, value)

def read_toml_config(config_file_name, section):

    main_logger.debug('config_file_name: %s', config_file_name)

    config_file = os.path.expanduser('~/.trrc') if not config_file_name \
                                                        else os.path.expanduser(config_file_name)
    main_logger.debug('config_file: %s', config_file)

    if section is None:
        main_logger.debug('default section')
        section = 'default'

    try:
        with open(config_file, "r", encoding="utf-8") as file_obj:
            toml_load = loads(file_obj.read())

    # if there is no ~/.trrc nor config_file_name, then return empty dict.
    except FileNotFoundError:
        main_logger.debug("can't open a config file: %s", config_file)
        if config_file_name is None:
            main_logger.debug('Use an empty dictionary instead of the default config file')
            return {}

        print(f"There is no '{config_file_name}'. Please check the config file name.", file=sys.stderr)
        sys.exit(1)

    except PermissionError:
        print(f"""Permission error: '{config_file}'.
Please check the permission of the file with 'ls -l {config_file}'.""", file=sys.stderr)
        sys.exit(1)

    try:
        main_logger.debug('load config: %s', toml_load[section])

        return toml_load[section]

    except exceptions.NonExistentKey:
        raise KeyError(f"There is No '{section}' section in the config file. Please check an alias of the config file.")

def mask_apikey(config: dict):
    """
    Mask apikey only if an apikey value exists.
    """

    # If key is key or apikey and v is not false nor None, then return 'masked'. In other cases, print as it is.
    return { k: ('masked' if k in {'key', 'apikey'} and v else v) for k, v in  config.items() }

def make_toml(parsed_arg: dict, section_title='untitled'):

    if not isinstance(parsed_arg, dict):
        parsed_arg = vars(parsed_arg)

    # if v has any value and k is not in the set, then generate a dict.
    return {section_title : {k: v for k, v in parsed_arg.items()
                             if v and
                             k not in {'cardContents',
                                       'alias',
                                       'config',
                                       'toml_generate',
                                       'toml_section',
                                       'toml_write'}}}

def toml_arg_handle(do_print_toml, config_file_name, section_title, parsed_arg):

    if config_file_name or do_print_toml:
        if section_title is None:
            section_title = 'untitled'
        toml = make_toml(parsed_arg, section_title)

        if do_print_toml:
            print(tomli_w.dumps(toml))

        if config_file_name:
            with open(config_file_name, "wb") as file_obj:
                tomli_w.dump(toml, file_obj)

        sys.exit(2)
