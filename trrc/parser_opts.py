"""module for parser using argparse"""
import argparse
import logging

VERSION_MESSAGE = """trrc - ToRRential Card processor 0.1.3
Copyright (C) 2023  Constantin Hong
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law."""

DESCRIPTION = "A command-line unix-like program to create Anki cards using AnkiConnect API."

CLOZE_TYPE_HELP = "Set a type of a fallback for a cloze type. The default is " \
"'cloze'. If user set --field option, then the default won't work. Even a string " \
"contains cloze, the program will process as a field unless user set " \
"--cloze-type"

CARD_CONTENT_HELP = "A quoted string divided by IFS. The default IFS is a tab character. " \
        "Instead of a string, it can also take a file consists of strings " \
        "without '--FILE' option. A [CARD_CONTENT] of '-' stands for standa" \
        "rd input."

def create_parser():
    """
    create parser
    """

    parser = argparse.ArgumentParser(
            prog='trrc',
            description=DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    parser.add_argument(
            'cardContents', action='store', nargs='*',
            metavar="CARD_CONTENT",
            help=CARD_CONTENT_HELP)

    parser.add_argument(
            '-D', '--deck',
            action='store', dest='deck',
            help=(
            "Set a Deck. The default is 'default'."
            ))

    parser.add_argument(
            '-t', '--type',
            action='store', dest='cardtype',
            help=(
            "Set a card type. The default is 'Basic'."
            ))

    parser.add_argument(
            '-i', '--ip',
            action='store', dest='ip',
            help=(
            "Set a ip that AnkiConnect specified. The default is '127.0.0.1'."
            ))

    parser.add_argument(
            '-p', '--port',
            action='store', dest='port', type=int,
            help=(
            "Set a port number that AnkiConnect specified. The default is '8765'."
            ))

    parser.add_argument(
            '-f', '--file',
            action='store', dest='file', nargs='*',
            help=(
            'Set a file that contains card contents.'
            ))

    parser.add_argument(
            '-c', '--config',
            metavar="FILE",
            action='store', dest='config',
            help=(
            "Set a config file to import config options. Without this option, " \
            "this program searches '~/.trrc', '$PWD/.trrc'."
            ))

    parser.add_argument(
            '--alias',
            metavar="SECTION",
            action='store', dest='alias',
            help=(
            "Set a section of a config file to apply options. Without this " \
            "argument, the default is 'default'."
            ))

    parser.add_argument(
            '-F', '--IFS',
            action='store', dest='ifs',
            help=(
            "Set a delimiter of card contents to use any character other than " \
            "a tab character. The default is a tab character."
            ))

    parser.add_argument(
            '--field',
            metavar="COLON:DELIMITER-SEPARATED:FIELDS",
            action='store', dest='field',
            help=(
            "Set a card field corresponding to the [CARD_CONTENT]. The default " \
            "is 'Front:Back:Tags'."
            ))

    parser.add_argument(
            '--cloze-field',
            metavar="COLON:DELIMITER-SEPARATED:FIELDS",
            action='store', dest='cloze_field',
            help=(
            "Set a cloze type card field corresponding to the [CARD_CONTENT]. " \
            "The default is 'Text:Back Extra:Tags'."
            ))

    parser.add_argument(
            '--cloze-type',
            action='store', dest='cloze_type',
            help=CLOZE_TYPE_HELP)

    parser.add_argument(
            '--toml-generate',
            action='store_true', dest='toml_generate',
            help=(
            "Print toml configs with current arguments. To set a section of " \
            "it, use it with '--toml-section' option."
            ))

    parser.add_argument(
            '--toml-write',
            metavar="FILE",
            action='store', dest='toml_write',
            help=(
            "Write a config file with options used. To set a section, use " \
            "'--toml-section'."
            ))

    parser.add_argument(
            '--toml-section',
            metavar="SECTION",
            action='store', dest='toml_section',
            help=(
            "Set a toml section. The default is 'untitled'."
            ))

    parser.add_argument(
            '-H', '--render-HTML',
            action='store_true', dest='allow_HTML',
            help=(
            "Set to allow to render a HTML tag. The default doesn't allow " \
            "render a HTML tag, therefore <br> won't be a new line."
            ))

    parser.add_argument(
            '--apikey',
            action='store', dest='apikey',
            help=(
            "Set an api key for AnkiConnect. If it is specified, --debug " \
            "option will mask it because of security concern."
            ))

    parser.add_argument(
            '--sync',
            action='store_true', dest='sync',
            help=(
            "Sync Anki. If there is a card to process, trrc syncs after " \
            "adding the card. The default is not to sync."
            ))

    parser.add_argument(
            '--force-add',
            action='store_true', dest='force_add',
            help=(
            "Create a card even if there is a duplicate in the deck."
            ))

    parser.add_argument(
            '--dry-run',
            action='store_true', dest='dryrun',
            help=(
            'Perform a trial run without sending to Anki.'
            ))

    parser.add_argument(
            '--read-file-in-a-content',
            action='store_true', dest='contents_file_import',
            help=(
            "Set to allow to replace a file in contents with its contents. A default setting doesn't read it"
            ))

    parser.add_argument(
            '-v', '--verbose',
            action='store_const', dest='verbose', const=logging.INFO,
            help=(
            'Print a card being currently processed.'
            ))

    parser.add_argument(
            '--debug', dest='debug', nargs='?', const=logging.DEBUG,
            metavar="FILE",
            help=(
            'Print debug information. If you specify FILE, trrc writes debug there.'
            ))

    parser.add_argument(
            '-V', '--version',
            action='version', dest='version', version=VERSION_MESSAGE,
            help=(
            'Print a version number and a license of trrc.'
            ))

    return parser
