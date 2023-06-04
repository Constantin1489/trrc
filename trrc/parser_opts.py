"""module for parser using argparse"""
import argparse
import logging

VERSION_MESSAGE = """trrc - ToRRential Card processor 0.1.1
Copyright (C) 2023  Constantin Hong
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law."""

DESCRIPTION = "A command line application to create Anki cards using AnkiConnect API."

CLOZE_TYPE_HELP = "set a type of a fallback for a cloze type. the default is " \
"'cloze'. if user set --field option, then the default won't work. even a string " \
"contains cloze, the program will process as a field unless user set " \
"--cloze-type"

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
            help=(
            "a string divided by IFS. the default IFS is a tab character. " \
            "instead of a string, It can also take a file consists of strings " \
            "without '--FILE' option."
            ))

    parser.add_argument(
            '-D', '--deck',
            action='store', dest='deck',
            help=(
            "set a Deck. the default is 'default'."
            ))

    parser.add_argument(
            '-t', '--type',
            action='store', dest='cardtype',
            help=(
            "set a card type. the default is 'Basic'."
            ))

    parser.add_argument(
            '-i', '--ip',
            action='store', dest='ip',
            help=(
            "set a ip that AnkiConnect specified. the default is '127.0.0.1'."
            ))

    parser.add_argument(
            '-p', '--port',
            action='store', dest='port', type=int,
            help=(
            "set a port number that AnkiConnect specified. the default is '8765'."
            ))

    parser.add_argument(
            '-f', '--file',
            action='store', dest='file', nargs='*',
            help=(
            'set a file that contains card contents.'
            ))

    parser.add_argument(
            '-c', '--config',
            metavar="FILE",
            action='store', dest='config',
            help=(
            "set a config file to import config options. without this option, " \
            "this program searches '~/.trrc'."
            ))

    parser.add_argument(
            '--alias',
            metavar="SECTION",
            action='store', dest='alias',
            help=(
            "set a section of a config file to apply options. without this " \
            "argument, the default is 'default'."
            ))

    parser.add_argument(
            '-F', '--IFS',
            action='store', dest='ifs',
            help=(
            "set a delimiter of card contents to use any character other than " \
            "a tab character. the default is a tab character."
            ))

    parser.add_argument(
            '--field',
            metavar="COLON:DELIMITER-SEPARATED:FIELDS",
            action='store', dest='field',
            help=(
            "set a card field corresponding to the cardContents. the default " \
            "is 'Front:Back:Tags'."
            ))

    parser.add_argument(
            '--cloze-field',
            metavar="COLON:DELIMITER-SEPARATED:FIELDS",
            action='store', dest='cloze_field',
            help=(
            "set a cloze type card field corresponding to the cardContents. " \
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
            "print toml configs with current arguments. to set a section of " \
            "it, use it with '--toml-section' option."
            ))

    parser.add_argument(
            '--toml-write',
            metavar="FILE",
            action='store', dest='toml_write',
            help=(
            "write a config file with options used. to set a section, use " \
            "'--toml-section'."
            ))

    parser.add_argument(
            '--toml-section',
            metavar="SECTION",
            action='store', dest='toml_section',
            help=(
            "set a toml section. the default is 'untitled'."
            ))

    parser.add_argument(
            '-H', '--render-HTML',
            action='store_true', dest='allow_HTML',
            help=(
            "set to allow to render a HTML tag. the default doesn't allow " \
            "render a HTML tag, therefore <br> won't be a new line."
            ))

    parser.add_argument(
            '--apikey',
            action='store', dest='apikey',
            help=(
            "set an api key for AnkiConnect. if it is specified, --debug " \
            "options will mask it because of security concern."
            ))

    parser.add_argument(
            '--sync',
            action='store_true', dest='sync',
            help=(
            "sync Anki. if there is a card to process, trrc syncs after " \
            "adding the card. the default is not to sync."
            ))

    parser.add_argument(
            '--force-add',
            action='store_true', dest='force_add',
            help=(
            "create a card even if there is a duplicate in the deck."
            ))

    parser.add_argument(
            '--dry-run',
            action='store_true', dest='dryrun',
            help=(
            'perform a trial run without sending to Anki.'
            ))

    parser.add_argument(
            '--read-file-in-a-content',
            action='store_true', dest='contents_file_import',
            help=(
            "set to allow to replace a file in contents with its contents. a default setting doesn't read it"
            ))

    parser.add_argument(
            '-v', '--verbose',
            action='store_const', dest='verbose', const=logging.INFO,
            help=(
            'print a card being currently processed.'
            ))

    parser.add_argument(
            '--debug', dest='debug', nargs='?', const=logging.DEBUG,
            metavar="FILE",
            help=(
            'print debug information. if you specify FILE, trrc writes debug there.'
            ))

    parser.add_argument(
            '-V', '--version',
            action='version', dest='version', version=VERSION_MESSAGE,
            help=(
            'print a version number and a license of trrc.'
            ))

    return parser
