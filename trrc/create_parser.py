import sys
import logging
import os
import re
import json
import requests
from .utils import (
        Card,
        card_str_regex_substitute,
        ErrorMessages,
        AnkiConnectInfo,
        error_message_coloring,
        RegexPattern)
from .parser_opts import create_parser
from .config_opts import (
        ParsedConfig,
        DEFAULT_CONFIG_FILES,
        read_toml_config,
        toml_arg_handle,
        mask_apikey)

main_logger = logging.getLogger(__name__)

def parse_argument(args=None):

    parser = create_parser()

    parsed_arg = parser.parse_args(args)

    # enable logger
    logger_level = get_logging_level(parsed_arg)
    debugger_type = type(logger_level)

    if debugger_type is int:
        logging.basicConfig(encoding='utf-8', level=logger_level)

    # if file to logging is specified
    if debugger_type is str:
        DEBUG_FILE = os.path.expanduser(parsed_arg.debug)
        logging.basicConfig(filename=DEBUG_FILE,
                            filemode='a',
                            encoding='utf-8',
                            level=logging.DEBUG)

    main_logger.debug('#######################################')

    # TOML
    if parsed_arg.toml_generate or parsed_arg.toml_write:
        toml_arg_handle(parsed_arg.toml_generate,
                        parsed_arg.toml_write,
                        parsed_arg.toml_section,
                        parsed_arg)

    main_logger.debug('arguments: %s, type: %s',
                      mask_apikey(vars(parsed_arg)), type(vars(parsed_arg)))

    # parse configs from default config files and user option arguments.
    options = parse_config(parsed_arg)

    if len(args) >= 1:

        cardcontents_handle(options)
        card_candidates = options.cardContents if options.cardContents else []

        # get contents from PIPE.
        if '-' in card_candidates:
            card_candidates.remove('-')

            for card in sys.stdin.readlines():

                # skip comment
                if card[0] == '#':
                    continue

                parsed_a_line = card.rstrip('\n')
                card_candidates.append(parsed_a_line)

            main_logger.debug('PIPE: %s', card_candidates)

    else:
        parser.print_help()
        sys.exit(2)

    return card_candidates, options

# if both debug and verbose options are on, then use debug.
def get_logging_level(parser):
    """
    This allows users to use both verbose and debug options.
    """

    if parser.debug is not None:
        return parser.debug
    if parser.verbose is not None:
        return parser.verbose

    return None

def get_proper_deck(argparse_deck=None):
    """
    get a card deck.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_deck:
        main_logger.debug('(argparse) deck is %s', argparse_deck)
        return argparse_deck

    if 'ANKIADDERALL_DECK' in os.environ:
        main_logger.debug("(env) deck is %s", os.environ['ANKIADDERALL_DECK'])
        return os.environ['ANKIADDERALL_DECK']

    main_logger.debug("(hard coded) deck is 'Default'")
    return 'Default'

def get_proper_cardtype(argparse_cardtype=None):
    """
    get a card type.
    order: card's deck & type => variables in bash file  OR export variables OR a temporary variable => (rc-file =>) hard coded defaults
    """

    if argparse_cardtype:
        main_logger.debug('(argparse) card type: %s', argparse_cardtype)
        return argparse_cardtype

    if 'ANKIADDERALL_TYPE' in os.environ:
        main_logger.debug('(osenv) type is %s', os.environ['ANKIADDERALL_TYPE'])
        return os.environ['ANKIADDERALL_TYPE']

    main_logger.debug("(hard coded) type is 'Basic'")
    return 'Basic'

def cardcontents_handle(options):
    """
    If card.cardContents is a file, then insert it into --file option.
    """

    files_in_cardcontents = []
    for i in options.cardContents:
        if os.path.isfile(i):
            main_logger.debug("File: %s, existance: %s", i, os.path.isfile(i))
            files_in_cardcontents.append(i)
            options.cardContents.remove(i)

    # if cardContents is a file, not a card contents, then put it in card.file.
    if files_in_cardcontents:
        for i in files_in_cardcontents:

            if options.file:
                options.file.append(i)

            # If card.file is None, then insert the list to --file option.
            else:
                options.file = [i]

    else:
        if options.cardContents:
            main_logger.debug("No file in card")
        else:
            main_logger.debug("Empty card")

    # if there is no card OR a sole fole --file option

# parse cards, card's deck and type in the input.
def parse_card(card_candidates, options):
    """
    Loop card_candidates to create cards.
    """

    ankiconnect_info = AnkiConnectInfo(options.ip, options.port, options.apikey)
    regexes = RegexPattern()

    if len(card_candidates) == 0:
        if options.sync:
            sync(ankiconnect_info.url, ankiconnect_info.apikey)
            sys.exit(0)

    notes = []
    notes.extend(gather_card_from(card_candidates, options, regexes))

    if options.file:
        main_logger.debug('file in option: %s', options.file)

        for afile in options.file:
            lines = []
            try:
                with open(afile, "r", encoding="utf-8") as file_obj:
                    lines += file_obj.read().splitlines()

            except FileNotFoundError:
                main_logger.debug('File not found: %s', afile)
                continue

            except PermissionError:
                print(f"""Permission error: '{afile}'.
Please check the permission of the file with 'ls -l {afile}'.""", file=sys.stderr)
                continue

            main_logger.debug('Read a file: %s', afile)

            notes.extend(gather_card_from(lines, options, regexes, afile))

    if options.dryrun is False:
        response = send_card_ankiconnect(ankiconnect_info.url,
                                         notes,
                                         'addNotes',
                                         ankiconnect_info.apikey)

        check_response(response.text, notes, ankiconnect_info.url, ankiconnect_info.apikey)

    if options.sync:
        sync(ankiconnect_info.url, ankiconnect_info.apikey)

def gather_card_from(card_candidates, options, regexes, filename=None):

    notes = []

    if filename is None:
        main_logger.debug("--file option off")

    for i, candidate in enumerate(card_candidates, start=1):

        # print a current card.
        main_logger.debug('string: %s', candidate)

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
            # Print current card and the line of a file if verbose option is on
            main_logger.info("%s:%s: %s",
                             filename, i, candidate)
        else:
            # Print current card If stdin, pipe or redirection
            main_logger.info("%s: %s", i, candidate)

        try:
            # if a line has cloze tag, than the line is a cloze type.
            notes.append(process_card(candidate, options, regexes))

        except AttributeError as err:
            if "'card' object has no attribute 'content'" in err.args:
                pass
            else:
                print(f"Unknown error: {err}", file=sys.stderr)
            continue

    return notes

def process_card(cardcontents: str, options, regex_compiles):

    modified_type: str = check_cloze_is_mistakely_there(cardcontents, options.cardtype)

    try:
        temp_card_obj = Card(get_proper_deck(options.deck),
                              modified_type,
                              cardcontents,
                              options.field,
                              options.cloze_field,
                              options.cloze_type,
                              options.ifs)

    except Exception as err:
        print(err, file=sys.stderr)
        print('failed: ' + cardcontents, file=sys.stderr)


    if options.allow_HTML is None:
        temp_card_obj.card_str = card_str_regex_substitute(temp_card_obj.card_str,
                                                           regex_compiles.prevent_html_interpret_compile,
                                                           regex_compiles.prevent_html_interpret_pattern)

    temp_card_obj.card_str = card_str_regex_substitute(temp_card_obj.card_str,
                                                       regex_compiles.newline_to_html_br_compile,
                                                       regex_compiles.newline_to_html_br_pattern)

    temp_card_obj.make_card()

    if options.contents_file_import is True:
        temp_card_obj.import_if_file_in_content(regex_compiles.str_to_html_compile,
                                                 regex_compiles.str_to_html_pattern)

    if options.force_add:
        card = temp_card_obj.create_cardjson_note()
        card.update({"options" : { "allowDuplicate": True, "duplicateScope": "deck"}})
        return card

    return temp_card_obj.create_cardjson_note()

def get_api_dict(action, parameter='', apikey=''):
    """Get AnkiConnect API obj"""

    dict_template = { 'addNote' : {"action" : "addNote",
                                   "version": 6,
                                   "params": { "note" : parameter },
                                   "key": apikey },
                     'addNotes' : {"action" : "addNotes",
                                   "version": 6,
                                   "params": { "notes" : parameter }},
                     'multi' : {"action" : "multi",
                                "version": 6,
                                "params": { "actions" : parameter }},
                     'get_type_name' : { "action": "modelNames",
                                        "version": 6 },
                     'get_deck_list' : { "action": "deckNames",
                                        "version": 6 },
                     'get_fields_of_model' : { "action": "modelFieldNames",
                                              "version": 6,
                                              "params": { "modelName": parameter }},
                     'sync' : {"action": "sync", "version": 6,'key' : parameter},
                     }

    return dict_template[action]

def send_card_ankiconnect(ankiconnect_url, card_json, action, apikey: str):

    # if apikey exist then update it
    jsonobj = get_api_dict(action, card_json)

    main_logger.debug('jsonobj: %s, type: %s', jsonobj, type(jsonobj))

    if apikey:
        jsonobj.update({'key' : apikey})

    try:

        DEFAULT_WAITING_CONNECTION_SEC = 5
        DEFAULT_WAITING_RESPONSE_READ_SEC = 40

        # If a number of the cards are over 100, then allow a longer time to
        # send a request.
        # if card_json: this allows to use send_card_ankiconnect generally
        if card_json and len(card_json) > 100:
            waiting_sec = len(card_json) // 100 + DEFAULT_WAITING_RESPONSE_READ_SEC
            timeout_value = (10, waiting_sec)
        else:
            # It's a default time to send a request.
            timeout_value = (DEFAULT_WAITING_CONNECTION_SEC,
                             DEFAULT_WAITING_RESPONSE_READ_SEC)

        main_logger.debug('timeout_value: %s, type: %s',
                          timeout_value, type(timeout_value))

        return requests.post(ankiconnect_url, json=jsonobj, timeout=timeout_value)

    except requests.exceptions.ReadTimeout:
        error_message_coloring(ErrorMessages.read_timed_out)

    except requests.exceptions.ConnectTimeout:
        error_message_coloring(ErrorMessages.connect_time_out)
        error_message_coloring(ankiconnect_url, 'AnkiConnect Target: ')
        error_message_coloring(ErrorMessages.ask_check_network)

    except requests.exceptions.ConnectionError:

        error_message_coloring(ankiconnect_url, 'AnkiConnect Target: ')
        error_message_coloring(ErrorMessages.ask_check_network)

    except requests.exceptions.InvalidURL:
        error_message_coloring(ankiconnect_url, 'Invalid url: ')
        # e.g.: --port 1212412412
        error_message_coloring('your port is wrong')

    # if exception occurs, exit.
    sys.exit(4)

def check_response(responsetext, card_json, ankiconnect_url, apikey):
    """
    Parse response text to debug if the AnkiConnect doesn't add the card.
    """

    fail_to_add_card_list = get_failed_card_from_response(responsetext,
                                                          card_json,
                                                          ankiconnect_url,
                                                          apikey)

    if len(fail_to_add_card_list) > 0:

        multi_failed_card = [ get_api_dict('addNote', card, apikey)
                             for card in fail_to_add_card_list ]

        multi_response = send_card_ankiconnect(ankiconnect_url,
                                               multi_failed_card,
                                               'multi',
                                               apikey)

        reasons = get_failed_card_from_multi_response(multi_response.text,
                                                      ankiconnect_url, apikey)

        for i, card in enumerate(fail_to_add_card_list):
            error_message_coloring(card, 'Failed: ')
            error_message_coloring(reasons[i], 'Reason: ')


        # INDIVIDUAL CARD ERROR REPORT
        reasons_set = {i['error'] for i in reasons.values()}
        print(f"\n#### Kinds of failures: {len(reasons_set)}")
        for i, v in enumerate(reasons_set, start=1):
            print(f'{i}: {v}')
            explain_error_response(v, ankiconnect_url, apikey)
        print("####")

    print(f"Total cards: {len(card_json)} " \
    f"Total fails: {len(fail_to_add_card_list)}", file=sys.stdout)

def get_failed_card_from_multi_response(res_str: str, ankiconnect_url, apikey):

    res_str_load: dict = json.loads(res_str)

    try:
        return dict(enumerate(res_str_load['result']))

    except KeyError as exc:
        # eg: res_str_load = { 'result': '', 'error': '' }
        explain_error_response(res_str_load['error'], ankiconnect_url, apikey)
        sys.exit(1)

def get_error_explanation_from_response(ankiconnect_url, card_json, action, apikey):
    res_str = send_card_ankiconnect(ankiconnect_url, card_json, action, apikey)
    res_str_load: dict = json.loads(res_str.text)

    if action == 'get_fields_of_model':
        return f"""--field '{':'.join(res_str_load['result'])}:Tags'

You don't have to use all those fields.
For example, if all fields of a type is 'Front:Back:Source:Sound:Tags'
you can use only some of them. e.g.: 'Front:Back:Tags'."""

    return res_str_load['result']

def explain_error_response(message_to_explain: str, ankiconnect_url, apikey):
    """
    print user-friendly explanation of the error message if the explanation exists.
    """

    ERROR_DICT = {
            "Minimum Anki version supported: 2.1.45": '',
            "Since Anki 2.1.28 it's not possible ": '',
            'Gui review is not currently active.': '',
            'Model name already exists': '',
            'Must provide a "fields" or "tags" property.': '',
            'Must provide at least one card for cardTemplates': '',
            'Must provide at least one field for inOrderFields': '',
            'Must provide tags as a list of strings': '',
            'The field values you have provided would make an empty question on all cards.': '',
            'You must provide a "data", "path", or "url" field.': '',
            'actions has invalid value': '',
            'cannot create note because it is a duplicate': "It's a duplicate. " \
                    "If you want to add it, use '--force-add' option. To view " \
                    "details of command, use '-h'",
            'cannot create note because it is empty': (ankiconnect_url, 'Basic', 'get_fields_of_model', apikey),
            'cannot create note for unknown reason': '',
            'collection is not available': '',
            'database is not available': '',
            'decks are not available': '',
            'media is not available': '',
            'option parameter "allowDuplicate" must be boolean': '',
            'option parameter "duplicateScopeOptions.checkAllModels" must be boolean': '',
            'option parameter "duplicateScopeOptions.checkChildren" must be boolean': '',
            'reviewer is not available': '',
            'scheduler is not available': '',
            'scopes has invalid value': '',
            'unsupported action': '',
            'valid api key must be provided': ErrorMessages.valid_api_key_require
            }

    ERROR_DICT_STARTSWITH = {
            'template was not found in': '',
            #'template was not found in {}: {}'
            'model was not found': (ankiconnect_url, '', 'get_type_name', apikey),
            #'model was not found: {}'
            'fontSize should be an integer': '',
            #'fontSize should be an integer: {}'
            'font should be a string': '',
            #'font should be a string: {}'
            'field was not found in': '',
            #'field was not found in {}: {}'
            'description should be a string': '',
            #'description should be a string: {}'
            'deck was not found':
            #'deck was not found: {}'
            (ankiconnect_url, '', 'get_deck_list', apikey)
            }

    if message_to_explain in ERROR_DICT:
        if ERROR_DICT[message_to_explain]:
            if type(ERROR_DICT[message_to_explain]) is not str:
                err_message = get_error_explanation_from_response(*ERROR_DICT[message_to_explain])
                error_message_coloring(err_message, 'trrc Tip')
            else:
                error_message_coloring(ERROR_DICT[message_to_explain], 'trrc Tip')
            return

        else:
            error_message_coloring('Please, report this issue to trrc github issue page',
                                   'Never Considered Error')
            error_message_coloring(message_to_explain, 'AnkiConnect')
            return

    for key in ERROR_DICT_STARTSWITH:
        if message_to_explain.startswith(key):
            # If no detailed explanation in the code, then just print it.
            if not ERROR_DICT_STARTSWITH[key]:
                error_message_coloring(message_to_explain, 'AnkiConnect')
                return
            if type(ERROR_DICT_STARTSWITH[key]) is not str:
                err_message = get_error_explanation_from_response(*ERROR_DICT_STARTSWITH[key])
                error_message_coloring(err_message, 'AnkiConnect')
            return

    error_message_coloring('Please, report this issue to trrc github issue page', 'Never Considered Error')
    error_message_coloring(message_to_explain, 'AnkiConnect')
    return


def get_failed_card_from_response(res_str: str, card_json: dict, ankiconnect_url, apikey):

    res_str_load: dict = json.loads(res_str)

    try:
        # if v is None, it is an error
        return [card_json[i] for i, v in enumerate(res_str_load['result']) if v is None]

    except TypeError as exc:
        # eg: res_str_load = { 'result': '', 'error': '' }
        # network error. So No result but error.
        explain_error_response(res_str_load['error'], ankiconnect_url, apikey)
        sys.exit(1)

def check_cloze_is_mistakely_there(card_contents: str, cardtype: str) -> str:
    """TODO: Docstring for check_cloze_is_mistakely_there.

    :card_contents: TODO
    :returns: TODO

    """

    if re.search(r'{{c\d+::.*}}', card_contents):
        main_logger.debug('found a cloze')
        return 'cloze'

    return get_proper_cardtype(cardtype)

def sync(ankiconnect_url, apikey=''):
    """
    Sync an anki.
    :ankiconnect_info: TODO
    """

    response = send_card_ankiconnect(ankiconnect_url, '', 'sync', apikey)

    if response.text == '{"result": null, "error": null}':
        print('sync: triggered')
        return

    check_response(response.text, '', ankiconnect_url, apikey)

DEFAULT_ALIAS = 'default'

def parse_config(parsed_arg):
    """Parse config options from default config files and user option argument."""

    # If user doesn't set section, then use 'default' even the config file is a
    # default config files or user config file.
    # So user can use both 'default' section of default config file and user
    # section of user config file.

    alias = parsed_arg.alias
    user_config_file = parsed_arg.config

    # parse hard coded options
    options = ParsedConfig(parsed_arg)
    main_logger.debug('hard coded options: %s', mask_apikey(vars(options)))

    # if there is no user config option then, read default config files.
    # this is a default routine.
    if not user_config_file:

        toml_configs = []
        found_section = {}
        alias_read = False

        # parse default config files
        for default_config in DEFAULT_CONFIG_FILES:

            toml_config = read_toml_config(default_config)
            found_section.update({default_config: [i for i in toml_config]})

            if DEFAULT_ALIAS in toml_config:
                main_logger.debug('section: default')
                toml_configs.append(toml_config[DEFAULT_ALIAS])

            # if alias is None type, then skip
            if alias and alias in toml_config:
                main_logger.debug('section: %s', alias)
                toml_configs.append(toml_config[alias])
                alias_read = True

        # if user set alias option but no alias found, then break.
        if alias and not alias_read:
            print(f"""There is no '{alias}' section in the config file.
Sections found: {found_section}""", file=sys.stderr)
            sys.exit(5)

        for i in toml_configs:
            options.overwrite_config(i)

    # if there is user config file, ignore default config files.
    if user_config_file:

        alias_read = False
        toml_configs = []
        toml_config = read_toml_config(user_config_file)
        found_section = {user_config_file: [i for i in toml_config]}

        main_logger.debug('TOML overwriting: %s', mask_apikey(vars(options)))

        if DEFAULT_ALIAS in toml_config:
            main_logger.debug('section: default')
            toml_configs.append(toml_config[DEFAULT_ALIAS])

        if alias and alias in toml_config:
            main_logger.debug('section: %s', alias)
            toml_configs.append(toml_config[alias])
            alias_read = True

        # if user set alias option but no alias found, then break.
        if alias and not alias_read:
            print(f"""There is no '{alias}' section in the config file.
Sections found: {found_section}""", file=sys.stderr)
            sys.exit(5)

        for i in toml_configs:
            options.overwrite_config(i)

    # finally overwrite argparse options
    options.overwrite_config(vars(parsed_arg))
    main_logger.debug('argument overwriting: %s', mask_apikey(vars(options)))

    return options
