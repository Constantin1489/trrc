import argparse
import sys
import requests
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import json
import ankiadderall.ankiadderall as ankiadderall
from ankiadderall.ankiadderall import bcolors, ErrorMessages, ErrorMessageColoring, Regex_Pattern
from ankiadderall.parserOpts import create_parser
from ankiadderall.configOpts import make_toml, parsed_config, read_toml_config, toml_arg_handle
from ankiadderall.configOpts import mask_apikey

import logging
main_logger = logging.getLogger(__name__)


# TODO: isn't it a main()?
def parse_argument(args=None):

    parser = create_parser()

    # enable logger
    if args is None:
        args = sys.argv[1:]
    parsed_arg = parser.parse_args(args)
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

    if len(args) >= 1 and sys.stdin.isatty() is True:

        cardcontentsHandle(options)
        card_candidates = options.cardContents if options.cardContents else []
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

def cardcontentsHandle(options):
    """
    If card.cardContents is a file, then insert it into --file option.
    """

    files_in_cardContents = []
    for i in options.cardContents:
        if os.path.isfile(i):
            main_logger.debug(f"{os.path.isfile(i)=}")
            files_in_cardContents.append(i)
            options.cardContents.remove(i)

    # if cardContents is a file, not a card contents, then put it in card.file.
    if files_in_cardContents:
        for i in files_in_cardContents:

            main_logger.debug(f"{i=}")

            if options.file :
                options.file.append(i)

            # If card.file is None, then insert the list to --file option.
            else:
                options.file = [i]

    else:
        if options.cardContents:
            main_logger.debug(f"No file in card")
        else:
            main_logger.debug(f"Empty card")

    # if there is no card OR a sole fole --file option

# parse cards, card's deck and type in the input.
def parse_card(card_candidates, options):
    """
    Loop card_candidates to create cards.
    """

    AnkiConnectInfo = ankiadderall.userAnkiConnect(options.ip,
                                                   options.port)

    regexes = Regex_Pattern()

    if len(card_candidates) == 0:
        if options.sync:
            sync(AnkiConnectInfo, options.apikey)
            exit(0)

    Notes = []
    Notes.extend(gather_card_from(card_candidates, options, regexes))

    if options.file:
        main_logger.debug(f'{options.file=}')

        for afile in options.file:
            lines = []
            try:
                with open(afile) as f:
                    lines += f.read().splitlines()
            except Exception as e:
                print(e, file=sys.stderr)

            main_logger.debug(f'read a file: {afile}')

            Notes.extend(gather_card_from(lines, options, regexes, afile))

    if options.dryrun is False:
        send_card_AnkiConnect(AnkiConnectInfo,
                              Notes,
                              options.apikey,
                              (options.verbose or options.debug))

    if options.sync:
        sync(AnkiConnectInfo, options.apikey)

def gather_card_from(card_candidates, options, regexes, filename=None):

    Notes = []

    if filename is None:
        main_logger.debug("--file option off")

    for i, candidate in enumerate(card_candidates, start=1):

        # print a current card.
        main_logger.debug(f'string: {candidate}')

        if not candidate:
            if filename:
                #this is a 'grep -n' style.
                print(f'{filename}:{i} is an empty line.', file=sys.stdout)
            else:
                print(f'line {i}: no card or a empty line', file=sys.stdout)
            continue

        # skipping comments
        if candidate[0] == '#':
            if filename:
                #this is a 'grep -n' style. this is useful when jumping between files using vim `gF`
                print(f'{filename}:{i} is a comment.', file=sys.stdout)
            else:
                print(f'line {i} is a comment.', file=sys.stdout)
            continue

        if filename:
            main_logger.info(f"{filename}:{i}: {candidate}")
        else:
            main_logger.info(f"{i}: {candidate}")

        try:
            # if a line has cloze tag, than the line is a cloze type.
            Notes.append(process_card(candidate, options, regexes))

        except AttributeError as e:
            if "'card' object has no attribute 'content'" in e.args:
                pass
            else:
                print(f"Unknown error: {e}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Failed to append a card: {e}", file=sys.stderr)
            continue

    return Notes

def process_card(cardcontents: str, options, regex_compiles):

    TYPE: str = check_cloze_is_mistakely_there(cardcontents, options.cardtype)

    try:
        tempCardObject = ankiadderall.card(get_proper_deck(options.deck),
                                           TYPE,
                                           cardcontents,
                                           options.field,
                                           options.cloze_field,
                                           options.cloze_type,
                                           options.IFS)

    except Exception as e:
        print(e, file=sys.stderr)
        print('failed: ' + cardcontents, file=sys.stderr)

    if options.contents_file_import is True:
        tempCardObject.import_if_file(regex_compiles.str_to_html_compile,
                                      regex_compiles.str_to_html_pattern)

    if options.allow_HTML is None:
        tempCardObject.card_str_regex_substitute(regex_compiles.prevent_HTML_interpret_compile,
                                                 regex_compiles.prevent_HTML_interpret_pattern)

    tempCardObject.card_str_regex_substitute(regex_compiles.newline_to_html_br_compile,
                                             regex_compiles.newline_to_html_br_pattern)

    tempCardObject.make_card()

    if options.force_add:
        card = tempCardObject.create_cardjson_note()
        card.update({"options" : { "allowDuplicate": True, "duplicateScope": "deck"}})
        return card

    return tempCardObject.create_cardjson_note()

#TODO: apikey
#TODO: CARD_JSON
def send_card_AnkiConnect(AnkiConnectInfo, CARD_JSON, apikey: str, verboseOrDebug: bool):

    # if apikey exist then update it
    jsonobj = { "action": "addNotes",
            "version": 6,
            "params": { "notes": CARD_JSON }}
    main_logger.debug(f'{jsonobj=}: {type(jsonobj)=}')

    if apikey:
        jsonobj.update({'key' : apikey})

    try:

        DEFAULT_WAITING_CONNECTION_SEC = 5
        DEFAULT_WAITING_RESPONSE_READ_SEC = 40

        # If a number of the cards are over 100, then allow a longer time to
        # send a request.
        if len(CARD_JSON) > 100:
            waiting_sec = len(CARD_JSON) // 100 + DEFAULT_WAITING_RESPONSE_READ_SEC
            timeout_value = (10, waiting_sec)
        else:
            # It's a default time to send a request.
            timeout_value = (DEFAULT_WAITING_CONNECTION_SEC,
                             DEFAULT_WAITING_RESPONSE_READ_SEC)

        main_logger.debug(f'{timeout_value=}: {type(timeout_value)=}')
        response = requests.post(AnkiConnectInfo, json=jsonobj, timeout=timeout_value)
        check_response(response.text, CARD_JSON, verboseOrDebug)

    except requests.exceptions.ReadTimeout as e:
        ErrorMessageColoring(ErrorMessages.read_timed_out)
        exit(4)
    except requests.exceptions.ConnectTimeout as e:
        ErrorMessageColoring(ErrorMessages.connect_time_out)
        ErrorMessageColoring(ErrorMessages.ask_check_network)
        exit(4)
    except requests.exceptions.ConnectionError as e:
        ErrorMessageColoring(ErrorMessages.ask_check_network)
        exit(4)
    except ValueError as e:
        print(e)
    except Exception as e:

        ErrorMessageColoring(e, 'ERROR')
        ErrorMessageColoring(ErrorMessages.unknown_network_error)
        # default network error message.
        ErrorMessageColoring(ErrorMessages.ask_check_network)
        exit(4)

def check_response(responsetext, CARD_JSON, verboseOrDebug):
    """
    Parse response text to debug if the AnkiConnect doesn't add the card.
    """

    fail_to_add_card_list = get_failed_card_from_response(responsetext, CARD_JSON)

    for i in fail_to_add_card_list:
        print(f"{bcolors.FAIL + bcolors.BOLD + 'Failed:' + bcolors.ENDC} {i}", file=sys.stderr)
    print(f"Total cards: {len(CARD_JSON)} Total fails: {len(fail_to_add_card_list)}", file=sys.stdout)

def get_failed_card_from_response(res_str: str, CARD_JSON: dict):

    res_str_load: dict = json.loads(res_str)
    try:
        return [CARD_JSON[i] for i, v in enumerate(res_str_load['result']) if v is None]
    except:
        if res_str_load['error'] == 'valid api key must be provided':
            ErrorMessageColoring(ErrorMessages.valid_api_key_require)
            exit(1)
        else:
            raise ValueError(f"{res_str_load['error']}")

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
    :AnkiConnectInfo: TODO
    """
    response = requests.post(AnkiConnectInfo, json={"action": "sync", "version": 6,'key' : apikey}, timeout=(1,1))
    print(f'sync: {response.text}')
