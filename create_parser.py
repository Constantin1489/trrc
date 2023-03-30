import argparse
# create_parser
def create_parser():
    """
     create_parser
    """

    parser = argparse.ArgumentParser(
            prog='Ankiadderall',
            description='a command line application to create anki cards',
            epilog='Constantin Hong'
            )

    #positional values
    parser.add_argument(
            'cardContents', action='store', nargs='?',
            help=(
            'a contents of a card'
            ))

    parser.add_argument(
            '-D', '--deck',
            action='store', dest='deck', default='Default',
            help=(
            'set a Deck.'
            ))

    parser.add_argument(
            '-t', '--type',
            action='store', dest='cardtype', default='basic',
            help=(
            'set a card type.'
            ))

    parser.add_argument(
            '-i', '--ip',
            action='store', dest='ip', default='127.0.0.1',
            help=(
            'set a AnkiConnect ip.'
            ))

    # mutually exclusive with positional value liked cardContents
    # ~/.acprc OR optional .acprc
    parser.add_argument(
            '-f', '--file',
            action='store', dest='file', nargs='*',
            help=(
            'set a ip.'
            ))

    # TODO : Execute configparse to a string object.
    parser.add_argument(
            '-c', '--config',
            action='store', dest='config',
            help=(
            'set a config.'
            ))

    # get an alias from a config file.
    # TODO : Execute configparse to a string object.
    parser.add_argument(
            '--alias',
            action='store', dest='alias',
            help=(
            'set an alias.'
            ))

    parser.add_argument(
            '-p', '--port',
            action='store', dest='port', type=int, default=8765,
            help=(
            'set a AnkiConnect port.'
            ))
    parser.add_argument(
            '-F', '--IFS',
            action='store', dest='IFS',
            help=(
            'a sed-like IFS option'
            ))

    return parser

# TODO: import config logic. card's deck & type => variables in bash file  OR export variables OR a temporary variable \
# => (rc-file =>) hard coded defaults
def get_proper_deck(argparse_deck, stdin_DECK):
    """
    get a card deck. 
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_deck:
        return argparse_deck

    if stdin_Deck:
        return stdin_Deck

    if rc_Deck:
        return rc_Deck

    # return a default deck
    return 'Default'

# TODO: import config logic. card's deck & type => variables in bash file  OR export variables OR a temporary variable \
# => (rc-file =>) hard coded defaults
def get_proper_cardType(argparse_cardType, stdin_cardType):
    """
    get a card type. 
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_cardType:
        return argparse_cardType

    if stdin_cardType:
        return stdin_cardType

    if rc_cardType:
        return rc_cardType

    # return a default cardType
    return 'basic'


