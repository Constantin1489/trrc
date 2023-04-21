import argparse
import sys
import requests
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import ankiadderall.ankiadderall as ankiadderall
from ankiadderall.ankiadderall import bcolors, ErrorMessages
from ankiadderall.parserOpts import create_parser
import logging
main_logger = logging.getLogger(__name__)

# TODO: isn't it a main()?
def parse_argument():

    parser = create_parser()

    if len(sys.argv) > 1 and sys.stdin.isatty() is True:

        card_candidates: List[parser] = [parser.parse_args(sys.argv[1:])]
        logging.basicConfig(encoding='utf-8', level=get_logging_level(card_candidates[0]))
        main_logger.debug('stdin: sys.stdin.isatty')
        return card_candidates

    else:

        if sys.stdin.isatty() is False:
            card_candidates = []
            for card in sys.stdin.readlines():
                parsed_a_line = parser.parse_args([card.rstrip('\n')] + sys.argv[1:])
                card_candidates.append(parsed_a_line)

            try:
                logging.basicConfig(encoding='utf-8', level=get_logging_level(card_candidates[0]))

            # if a pipe redirection is only an empty line, run exception.
            except:
                if '--debug' in sys.argv[1:]:
                    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
                elif ('--verbose' or '-v') in sys.argv[1:]:
                    logging.basicConfig(encoding='utf-8', level=logging.INFO)

                print(f'no card or a empty line', file=sys.stderr)

            main_logger.debug('Pipe redirection: not sys.stdin.isatty.')

            return card_candidates

        else:
            parser.print_help()
            exit(2)

# if both debug and verbose options are on, then use debug.
def get_logging_level(parser):
    """
    This allows users to use both verbose and debug options.
    """

    if parser.debug is not None:
        return parser.debug
    elif parser.verbose is not None:
        return parser.verbose
    else:
        return None

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

    # if cardContents is a file, not a card contents, then put it in card.file.
    if card.cardContents and os.path.isfile(card.cardContents):

        main_logger.debug(f"{os.path.isfile(card.cardContents)=}")

        if card.file :
            card.file.append(card.cardContents)

        # If card.file is None, then insert the list to --file option.
        else:
            card.file = [card.cardContents]
        card.cardContents = None

    else:
        if card.cardContents:
            main_logger.debug(f"No file in card.CardContents")
        else:
            main_logger.debug(f"empty card.CardContents")

    # if there is no card OR a sole fole --file option
    return card

# parse cards, card's deck and type in the input.
def parse_card(card_candidates):
    """
    Loop card_candidates to create cards.
    """

    for candidate in card_candidates:

        # print a current card.
        main_logger.debug(f'string: {candidate.cardContents}')
        candidate = cardcontentsHandle(candidate)
        AnkiConnectInfo = ankiadderall.userAnkiConnect(candidate.ip,
                                                       candidate.port)
        if candidate.file:
            main_logger.debug(f'{candidate.file=}')

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
                process_card(j, candidate, AnkiConnectInfo)

        else:
            if not candidate.cardContents:
                print(f'no card or a empty line', file=sys.stderr)
                continue

            main_logger.debug("--file option off")

            try:
                process_card(candidate.cardContents, candidate, AnkiConnectInfo)
            except:
                continue

def process_card(cardcontents, candidate, AnkiConnectInfo):
    # if a line has cloze tag, than the line is a cloze type.
    TYPE = check_cloze_is_mistakely_there(cardcontents, candidate.cardtype)
    try:
        tempCardObject = ankiadderall.card(get_proper_deck(candidate.deck),
                                           TYPE,
                                           cardcontents,
                                           candidate.column,
                                           candidate.IFS)

    except Exception as e:
        print('failed: ' + cardcontents)

    main_logger.info(f'{tempCardObject.json}')
    send_card_AnkiConnect(AnkiConnectInfo, tempCardObject.json, candidate.dryrun)

def send_card_AnkiConnect(AnkiConnectInfo, CARD_JSON, dryrun):

    print(f'{CARD_JSON}', end='\r' )

    if dryrun is not True:
        try:
            response = requests.post(AnkiConnectInfo, json=CARD_JSON, timeout=(1,1))
            print('')
            check_response(response.text)

        except:
        # if the requests statements failed, then alert.
            print(bcolors.FAIL + bcolors.BOLD + ErrorMessages.network + bcolors.ENDC, file=sys.stderr)
            exit(4)

    else:
        # close carriage return
        print('')

def check_response(responsetext):
    """
    Parse response text to debug if the AnkiConnect doesn't add the card.
    """

    match_result = re.match('^{"result": (.*), "error": (.*)}', responsetext)
    if match_result.group(1) == 'null':
        print(bcolors.FAIL + bcolors.BOLD + match_result.group(2) + bcolors.ENDC, file=sys.stderr)

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
