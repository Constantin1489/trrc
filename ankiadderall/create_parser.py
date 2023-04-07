import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import ankiadderall.ankiadderall as ankiadderall
from ankiadderall.parserOpts import create_parser
import logging
main_logger = logging.getLogger(__name__)

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
def parse_card(card_candidates):

    for candidate in card_candidates:

        # print a current card.
        print(candidate.cardContents, end='\r')
        candidate = cardcontentsHandle(candidate)
        AnkiConnectInfo = ankiadderall.userAnkiConnect(candidate.ip,
                                                       candidate.port)
        if candidate.file:
            print(candidate.file, file=sys.stdout)

            lines = []
            for afile in candidate.file:
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
                TYPE = check_cloze_is_mistakely_there(j, candidate.cardtype)
                try:
                    tempCardObject = ankiadderall.card(get_proper_deck(candidate.deck),
                                                       TYPE,
                                                       j,
                                                       candidate.column,
                                                       candidate.IFS)
                except Exception as e:
                    print('failed: ' + card.cardContents)
                    continue

                if candidate.dryrun is not True:
                    ankiadderall.create_card(AnkiConnectInfo,
                                             tempCardObject)


        else:
            if not candidate.cardContents:
                main_logger.debug(f'no card or a empty line')
                continue

            main_logger.debug("It's not a file")

            TYPE = check_cloze_is_mistakely_there(candidate.cardContents,
                                                  candidate.cardtype)

            try:
                tempCardObject = ankiadderall.card(get_proper_deck(candidate.deck),
                                                   TYPE,
                                                   candidate.cardContents,
                                                   candidate.column,
                                                   candidate.IFS)
            except Exception as e:
                print(f'failed: {card.cardContents}')
                print(e, file=sys.stderr)
                continue

            if candidate.dryrun is not True:
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
