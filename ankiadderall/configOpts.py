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
        self.field = None
        self.file = None
        self.dryrun = False
        self.verbose = None
        self.debug = None

    def overwrite_config(self, configparse: dict, section_title=None):
        """
        Overwrites options of a config file with arg parser options
        """

        if section_title is None:
            main_logger.debug(f'{section_title=}')

            if configparse is None:
                # this doesn't affect existing attributes
                main_logger.debug('No configs')
                return

            # if configparse is a parser object, then make it a dict
            if not isinstance(configparse, dict):
                configparse = vars(configparse)

            main_logger.debug(f'{mask_apikey(configparse)=}')

            for k, v in configparse.items():
                if v is not None and v is not False:
                    setattr(self, k, v)
            main_logger.debug(f'{section_title=}')

        else:
            for k, v in make_toml(configparse, section_title)[section_title].items():
                if v is not None:
                    setattr(self, k, v)

def read_toml_config(config_file_name, section):

    main_logger.debug(f'{config_file_name=}')

    config_file = os.path.expanduser('~/.asprc') if not config_file_name \
                                                        else os.path.expanduser(config_file_name)
    main_logger.debug(f'{config_file=}')

    if section is None:
        main_logger.debug(f'default section')
        section = 'default'

    from tomlkit import loads, exceptions
    try:
        with open(config_file, "r") as f:
            toml_load = loads(f.read())

    # if there is no ~/.asprc nor config_file_name, then return empty dict.
    except FileNotFoundError as e:
        main_logger.debug(f"can't open a default {config_file}")
        if config_file_name is None:
            main_logger.debug(f"Use an empty dictionary instead of the default config file")
            return {}
        else:
            print(f"There is no '{config_file_name}'. Please check the config file name.", file=sys.stderr)
            exit(1)

    except PermissionError as p:
        print(f"""Permission error: '{config_file}'.
Please check the permission of the file with 'ls -l {config_file}'.""", file=sys.stderr)
        exit(1)
    except Exception as e:
        print(e)
        exit(1)

    try:
        main_logger.debug(f'{mask_apikey(toml_load[section])=}')

        return toml_load[section]

    except exceptions.NonExistentKey:
        raise KeyError(f"There is No '{section}' section in the config file. Please check an alias of the config file.")

    except Exception as e:
        print(f"Unknown Error: {e}")
        exit(1)

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

def toml_arg_handle(Do_print_toml, config_file_name, section_title, parsed_arg):

    if config_file_name or Do_print_toml:
        if section_title is None:
            section_title = 'untitled'
        toml = make_toml(parsed_arg, section_title)

        if Do_print_toml:
            print(tomli_w.dumps(toml))

        if config_file_name:
            with open(config_file_name, "wb") as f:
                tomli_w.dump(toml, f)

        exit(2)
