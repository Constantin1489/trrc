import argparse
import sys
sys.path.append('/Users/constantinhong/TODO/ankiadderall')
import os
import re
import ankiadderall
import logging
main_logger = logging.getLogger(__name__)

def create_parser():
    """
    create_parser
    """

    example_text="""
EXAMPLE
    pourc '안녕\\tHello\\tKorean'
    pourc --IFS % '안녕%Hello%Korean'
    pourc --column 'ArbitraryFourthFieldName:ArbitrarysecondFieldName:tag' 'FourthContent\tsecondContent\ttag'
    pourc --ip 192.168.1.230 --port 4832 --debug --file Korean_English_conversation.txt
    echo 'basic_type_front_normal_tab with option\\tbasic_type_back\\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

"""

    parser = argparse.ArgumentParser(
            prog='Ankiadderall',
            description='a command line application to create anki cards',
            epilog=example_text,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    parser.add_argument(
            'cardContents', action='store', nargs='?',
            help=(
            'a positional contents of a card'
            ))

    # TODO: LOCALE
    parser.add_argument(
            '-D', '--deck',
            action='store', dest='deck',
            help=(
            'set a Deck.'
            ))

    # TODO: LOCALE
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
            action='store', dest='IFS', default='\t',
            help=(
            'a sed-like IFS option'
            ))

    parser.add_argument(
            '--column', action='store', dest='column', nargs='?',
            type=lambda s: [i for i in s.split(':')],
            help=(
            'a positional contents of a card'
            ))

    parser.add_argument(
            '--dry-run',
            action='store_true', dest='dryrun',
            help=(
            'Print the cards that would be created and options that would be applied, but do not execute the command.'
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

    if len(sys.argv) > 1 and sys.stdin.isatty() is True:

        # TODO: logging
        if '--debug' in sys.argv[1:]:
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

        main_logger.debug('sys.stdin.isatty')
        card_candidate: List[parser] = [parser.parse_args(sys.argv[1:])]
        return card_candidate

    else:
        if '--debug' in sys.argv[1:]:
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

        if sys.stdin.isatty() is False:
            main_logger.debug('not sys.stdin.isatty')
            card_candidate = []
            for card in sys.stdin.readlines():
                parsed_a_line = parser.parse_args([card.rstrip('\n')] + sys.argv[1:])
                card_candidate.append(parsed_a_line)

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
        main_logger.debug(f'deck is {argparse_deck}')
        return argparse_deck

    if 'ANKIADDERALL_DECK' in os.environ.keys():
        main_logger.debug(f"deck is {os.environ['ANKIADDERALL_DECK']}")
        return os.environ['ANKIADDERALL_DECK']

# TODO: after configparse option developed, fix stdin_deck
# TODO: configparse
#    if rc_Deck:
#        main_logger.debug('rc_Deck is on')
#        return rc_Deck

    # return a default deck
    main_logger.debug(f"deck is 'Default'")
    return 'Default'

# TODO: import config logic. card's deck & type => variables in bash file  OR export variables OR a temporary variable \
# => (rc-file =>) hard coded defaults
def get_proper_cardType(argparse_cardType=None):
    """
    get a card type.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_cardType:
        main_logger.debug(f'type is {argparse_cardType}')
        return argparse_cardType

    if 'ANKIADDERALL_TYPE' in os.environ.keys():
        main_logger.debug(f"type is {os.environ['ANKIADDERALL_DECK']}")
        return os.environ['ANKIADDERALL_TYPE']

# TODO: configparse
#    if rc_cardType:
#        return rc_cardType

    # return a default cardType
    # TODO: the default term depends on the language user uses may vary.
    # ex) Korean -> '기본'
    main_logger.debug(f"type is 'Basic'")
    return 'Basic'

def cardcontentsHandle(card):
    """
    If card.cardContents is a file, then insert it into --file option.
    """

    if card.cardContents and os.path.isfile(card.cardContents):

        if card.file :
            card.file.append(card.cardContents)

        # If card.file is None, then insert the list to --file option.
        else:
            card.file = [card.cardContents]
        card.cardContents = None

    # if there is no card OR a sole fole --file option
    return card

# parse cards, card's deck and type in the input.
def parse_card(card_candidate):

    for card in card_candidate:

        # print a current card.
        print(card.cardContents, end='\r')
        card = cardcontentsHandle(card)

        if card.file:
            print(card.file, file=sys.stdout)

            lines = []
            for afile in card.file:
                with open(afile) as f:
                    lines += f.read().splitlines()

            main_logger.debug('read a file')

            for j in lines:

                # skipping an empty line.
                if not j:
                    print(f'empty line: {j}', file=sys.stdout)
                    main_logger.debug('skip a line')
                    continue

                # if a line has cloze tag, than the line is a cloze type.
                TYPE = check_cloze_is_mistakely_there(j, card.cardtype)
                tempCardObject = ankiadderall.card(get_proper_deck(card.deck),
                                                   TYPE,
                                                   j,
                                                   card.column,
                                                   card.IFS)
                AnkiConnectInfo = ankiadderall.userAnkiConnect(card.ip, card.port).get_AnkiConnect_URL()
                if not card.dryrun:
                    ankiadderall.create_card(AnkiConnectInfo, tempCardObject)


        else:
            if not card.cardContents:
                main_logger.debug(f'no card or a empty line')
                continue

            TYPE = check_cloze_is_mistakely_there(card.cardContents, card.cardtype)

            tempCardObject = ankiadderall.card(get_proper_deck(card.deck),
                                               TYPE,
                                               card.cardContents,
                                               card.column,
                                               card.IFS)

            AnkiConnectInfo = ankiadderall.userAnkiConnect(card.ip, card.port)
            if not card.dryrun:
                ankiadderall.create_card(AnkiConnectInfo, tempCardObject)

def check_cloze_is_mistakely_there(card_contents: str, cardtype: str) -> str:
    """TODO: Docstring for check_cloze_is_mistakely_there.

    :card_contents: TODO
    :returns: TODO

    """

    if re.findall(r'{{c\d::.*}}', card_contents):
        main_logger.debug('found a cloze')
        return 'cloze'
    else:
        return get_proper_cardType(cardtype)
