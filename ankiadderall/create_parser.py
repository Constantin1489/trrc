import argparse
import sys
import requests
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import json
import ankiadderall.ankiadderall as ankiadderall
from ankiadderall.ankiadderall import bcolors, ErrorMessages
from ankiadderall.parserOpts import create_parser
from ankiadderall.configOpts import make_toml, parsed_config, read_toml_config, toml_arg_handle
from ankiadderall.configOpts import mask_apikey

import logging
main_logger = logging.getLogger(__name__)


# TODO: isn't it a main()?
def parse_argument():

    parser = create_parser()

    # enable logger
    parsed_arg = parser.parse_args(sys.argv[1:])
    logging.basicConfig(encoding='utf-8', level=get_logging_level(parsed_arg))

    # TOML
    if parsed_arg.toml_generate or parsed_arg.toml_write:
        toml_arg_handle(parsed_arg.toml_generate, parsed_arg.toml_write, parsed_arg.toml_section, parsed_arg)

    main_logger.debug(f'arguments : {mask_apikey(vars(parsed_arg))=} = {type(vars(parsed_arg))=}')

    # parse hard coded options
    options = parsed_config(parsed_arg)
    main_logger.debug(f'hard coded options: {mask_apikey(vars(options))=}')

    # parse config file
    options.overwrite_config(read_toml_config(parsed_arg.config, parsed_arg.alias))
    main_logger.debug(f'TOML overwriting: {mask_apikey(vars(options))=}')

    # TODO: parse environment variables

    # overwrite argparse options
    options.overwrite_config(vars(parsed_arg))
    main_logger.debug(f'argument overwriting: {mask_apikey(vars(options))=}')


    if len(sys.argv) > 1 and sys.stdin.isatty() is True:

        card_candidates = [options.cardContents]
        main_logger.debug('stdin: sys.stdin.isatty')

    else:

        if sys.stdin.isatty() is False:

            card_candidates = []
            for card in sys.stdin.readlines():

                # skip comment
                if card[0] == '#':
                    continue

                parsed_a_line = card.rstrip('\n')
                card_candidates.append(parsed_a_line)

            main_logger.debug('Pipe redirection: not sys.stdin.isatty.')

        else:
            parser.print_help()
            exit(2)

    return card_candidates, options

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

def get_proper_deck(argparse_deck=None):
    """
    get a card deck.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_deck:
        main_logger.debug(f'(argparse) deck is {argparse_deck}')
        return argparse_deck

    if 'ANKIADDERALL_DECK' in os.environ.keys():
        main_logger.debug(f"(env) deck is {os.environ['ANKIADDERALL_DECK']}")
        return os.environ['ANKIADDERALL_DECK']

    main_logger.debug(f"(hard coded) deck is 'Default'")
    return 'Default'

def get_proper_cardType(argparse_cardType=None):
    """
    get a card type.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_cardType:
        main_logger.debug(f'(argparse) type is {argparse_cardType}')
        return argparse_cardType

    if 'ANKIADDERALL_TYPE' in os.environ.keys():
        main_logger.debug(f"(osenv) type is {os.environ['ANKIADDERALL_TYPE']}")
        return os.environ['ANKIADDERALL_TYPE']

    # TODO: the default term depends on the language user uses may vary.
    # ex) Korean -> '기본'
    main_logger.debug(f"(hard coded) type is 'Basic'")
    return 'Basic'

def cardcontentsHandle(card, options):
    """
    If card.cardContents is a file, then insert it into --file option.
    """

    # if cardContents is a file, not a card contents, then put it in card.file.
    if card and os.path.isfile(card):

        main_logger.debug(f"{os.path.isfile(card)=}")

        if options.file :
            options.file.append(card)

        # If card.file is None, then insert the list to --file option.
        else:
            options.file = [card]
        card = None

    else:
        if card:
            main_logger.debug(f"No file in card")
        else:
            main_logger.debug(f"empty card")

    # if there is no card OR a sole fole --file option
    return card

# parse cards, card's deck and type in the input.
def parse_card(card_candidates, options):
    """
    Loop card_candidates to create cards.
    """

    AnkiConnectInfo = ankiadderall.userAnkiConnect(options.ip,
                                                   options.port)

    if len(card_candidates) == 0:
        if options.sync:
            sync(AnkiConnectInfo, options.apikey)
            exit(0)

    for candidate in card_candidates:

        # print a current card.
        main_logger.debug(f'string: {candidate}')
        candidate = cardcontentsHandle(candidate, options)

        if options.file:
            main_logger.debug(f'{options.file=}')

            lines = []
            for afile in options.file:
                if os.path.isfile(afile):
                    with open(afile) as f:
                        lines += f.read().splitlines()

            main_logger.debug('read a file')

            for j in lines:

                # skipping an empty line.
                if not j:
                    print(f'empty line', file=sys.stdout)
                    continue

                # skipping comments
                if j[0] == '#':
                    main_logger.debug(f'skip a comment line: {j}')
                    continue

                # if a line has cloze tag, than the line is a cloze type.
                process_card(j, options, AnkiConnectInfo)

        else:
            if not candidate:
                print(f'no card or a empty line', file=sys.stderr)
                continue

            main_logger.debug("--file option off")

            try:
                process_card(candidate, options, AnkiConnectInfo)
            except:
                continue

    if options.sync:
        sync(AnkiConnectInfo, options.apikey)

def process_card(cardcontents, options, AnkiConnectInfo):

    TYPE = check_cloze_is_mistakely_there(cardcontents, options.cardtype)

    try:
        tempCardObject = ankiadderall.card(get_proper_deck(options.deck),
                                           TYPE,
                                           cardcontents,
                                           options.column,
                                           options.IFS)

    except Exception as e:
        print('failed: ' + cardcontents, file=sys.stderr)

    if options.contents_file_import is True:
        tempCardObject.import_if_file()

    if options.allow_HTML is False:
        tempCardObject.prevent_HTML_interpret()

    tempCardObject.newline_to_html_br()
    tempCardObject.make_card()
    tempCardObject.create_cardjson()

    main_logger.info(f'{tempCardObject.json}')

    if options.dryrun is False:
        send_card_AnkiConnect(AnkiConnectInfo,
                              tempCardObject.json,
                              options.apikey,
                              (options.verbose or options.debug))

#TODO: apikey
#TODO: CARD_JSON
def send_card_AnkiConnect(AnkiConnectInfo, CARD_JSON, apikey: str, verboseOrDebug: bool):

    # if apikey exist then update it
    CARD_JSON.update({'key' : apikey}) if apikey else None

    try:
        response = requests.post(AnkiConnectInfo, json=CARD_JSON, timeout=(1,1))
        check_response(response.text, CARD_JSON, verboseOrDebug)

    except:
        # if the requests statements failed, then alert.
        # raise?
        print(bcolors.FAIL + bcolors.BOLD + ErrorMessages.network + bcolors.ENDC, file=sys.stderr)
        exit(4)

def check_response(responsetext, json, verboseOrDebug):
    """
    Parse response text to debug if the AnkiConnect doesn't add the card.
    """

    match_result = re.match('^{"result": (.*), "error": (.*)}', responsetext)
    if match_result.group(1) == 'null':

        if verboseOrDebug is None:
            print(mask_apikey(json), file=sys.stderr)
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

def sync(AnkiConnectInfo, apikey=''):
    """
    Sync an anki.
    """
    response = requests.post(AnkiConnectInfo, json={"action": "sync", "version": 6,'key' : apikey}, timeout=(1,1))
