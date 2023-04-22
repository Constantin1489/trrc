import configparser


class parsed_config:

    """class for read config

    Other functions retrieve attributes from this class.

    """

    def __init__(self, configparser):
        """TODO: to be defined. """

        self.deck = configparser.deck
        self.cardtype = configparser.cardtype
        self.ip = configparser.ip
        self.port = configparser.port
        self.IFS = configparser.IFS
        self.column = configparser.column
        self.dryrun = configparser.dryrun
        self.verbose = configparser.verbose
        self.debug = configparser.debug

def init_config():
    """config initialization when start the application.
    :returns: TODO

    """
    pass

def read_config(configFile):
    """read a custome config file

    Args:
        configFile: string
    Returns:

    """
    pass

def write_config(configparser, configFile):
    """ write config.
    Args:
        configparser: 
        configFile: 

    Returns:
        None

    """
    pass

def print_config(config):
    """print config as stdout

    Args:
        config: TODO
    Returns:
        TODO

    """
    pass
