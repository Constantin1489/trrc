import argparse
import sys
sys.path.append('/Users/constantinhong/TODO/ankiadderall')
import os
import re
import ankiadderall
import logging

def create_parser():
    """
    create_parser
    """

    parser = argparse.ArgumentParser(
            prog='Ankiadderall',
            description='a command line application to create anki cards',
            epilog='Constantin Hong'
            )

    parser.add_argument(
            'cardContents', action='store', nargs='?',
            help=(
            'a positional contents of a card'
            ))

    # TODO: fix default
    parser.add_argument(
            '-D', '--deck',
            action='store', dest='deck',
            help=(
            'set a Deck.'
            ))

    # TODO: fix default
    parser.add_argument(
            '-t', '--type',
            action='store', dest='cardtype',
            help=(
            'set a card type.'
            ))

    parser.add_argument(
            '-i', '--ip',
            action='store', dest='ip', default='127.0.0.1',
            help=(
            'set a AnkiConnect ip.'
            ))

    parser.add_argument(
            '-p', '--port',
            action='store', dest='port', type=int, default=8765,
            help=(
            'set a AnkiConnect port.'
            ))

    parser.add_argument(
            '-f', '--file',
            action='store', dest='file', nargs='*',
            help=(
            'set a file to create cards.'
            ))

    # ~/.acprc OR optional .acprc
    # parser.file: List
    # TODO : Execute configparse to a string object.
    parser.add_argument(
            '-c', '--config',
            action='store', dest='config',
            help=(
            'set a config.'
            ))

    # get an alias from a config file.
    # looking for ~/.acprc OR ANKIADDERALL_CONFIG
    # TODO : Execute configparse to a string object.
    parser.add_argument(
            '--alias',
            action='store', dest='alias',
            help=(
            'set an alias.'
            ))

    parser.add_argument(
            '-F', '--IFS',
            action='store', dest='IFS',
            help=(
            'a sed-like IFS option'
            ))

    parser.add_argument(
            '--debug',
            action='store_const', dest='debug', const=logging.DEBUG,
            help=(
            'a debug option'
            ))

    return parser

# TODO: test argparse
# TODO: isn't it a main()?
def parse_argument():

    parser = create_parser()

    if len(sys.argv) > 1 and sys.stdin.isatty():

        # TODO: logging
        if '--debug' in sys.argv[1:]:
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

        main_logger = logging.getLogger(__name__)
        card_candidate: List[parser] = [parser.parse_args(sys.argv[1:])]
        return card_candidate

    else:
        if '--debug' in sys.argv[1:]:
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
        main_logger = logging.getLogger(__name__)

        if not sys.stdin.isatty():
            card_candidate = []
            for card in sys.stdin.readlines():
                some = [card.rstrip('\n')] + sys.argv[1:]
                card_candidate.append(parser.parse_args(some))

            return card_candidate

        else:
            parser.print_help()
            exit(2)


# TODO: import config logic. card's deck & type => variables in bash file  OR export variables OR a temporary variable \
# => (rc-file =>) hard coded defaults
def get_proper_deck(argparse_deck=None):
    """
    get a card deck.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_deck:
        return argparse_deck

    ANKIADDERALL_CONFIG = { 'DECK': 'Linux', 'TYPE':'Basic'  }
    stdin_Deck = os.environ['ANKIADDERALL_DECK'] if 'ANKIADDERALL_DECK' in os.environ.keys() else ANKIADDERALL_CONFIG['DECK']
    if stdin_Deck:
        return stdin_Deck

# TODO: configparse
#    if rc_Deck:
#        return rc_Deck

    # return a default deck
    return 'Default'

# TODO: import config logic. card's deck & type => variables in bash file  OR export variables OR a temporary variable \
# => (rc-file =>) hard coded defaults
def get_proper_cardType(argparse_cardType=None):
    """
    get a card type.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_cardType:
        return argparse_cardType

    ANKIADDERALL_CONFIG = { 'DECK': 'Linux', 'TYPE':'Basic'  }
    stdin_cardType = os.environ['ANKIADDERALL_TYPE'] if 'ANKIADDERALL_TYPE' in os.environ.keys() else ANKIADDERALL_CONFIG['TYPE']
    if stdin_cardType:
        return stdin_cardType

# TODO: configparse
#    if rc_cardType:
#        return rc_cardType

    # return a default cardType
    # TODO: fix default
    # TODO: the default term depends on the language user uses may vary.
    # ex) Korean -> '기본'
    return 'basic'

def cardcontentsHandle(card):
    """
    TODO: Docstring for fileHandle.
    """

    if card.cardContents and os.path.isfile(card.cardContents):
        if card.file :
            card.file.append(card.cardContents)
        else:
            card.file = [card.cardContents]
        card.cardContents = None

    return card

# parse cards, card's deck and type in the input.
def parse_card(card_candidate):

    for card in card_candidate:

        card = cardcontentsHandle(card)
        # TODO: file argparse exclusive with positional?
        if card.file:
            #and os.path.isfile(card.file)
            # logging?
            print(card.file, file=sys.stdout)

            lines = []
            for afile in card.file:
                with open(afile) as f:
                    lines += f.read().splitlines()

            for j in lines:

                # skipping an empty line.
                if not j:
                    continue

                # if a line has cloze tag, than the line is a cloze type.
                # note type handler
                if re.findall(r'{{c\d::.*}}', j):
                    TYPE = 'cloze'

                a = ankiadderall.card(get_proper_deck(card.deck), get_proper_cardType(card.cardtype), j)
                ankiadderall.create_card(ankiadderall.userAnkiConnect().get_AnkiConnect_URL(), a)
                print(a.card, file=sys.stdout)


        else:
            # TODO: ERROR #main_logger.debug(f'######## {card_candidate=}\n{type(card_candidate)=}')
            a = ankiadderall.card(get_proper_deck(card.deck), get_proper_cardType(card.cardtype), card.cardContents)
            ankiadderall.create_card(ankiadderall.userAnkiConnect().get_AnkiConnect_URL(), a)
            print(a.card, file=sys.stdout)
