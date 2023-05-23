import argparse
import logging
import sys
import os

VERSION = """%(prog)s 0.1.0 Copyright (C) 2023  Constantin Hong
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law."""

def create_parser():
    """
    create_parser
    """

    parser = argparse.ArgumentParser(
            prog='pourc',
            description='a command line application to create anki cards',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    parser.add_argument(
            'cardContents', action='store', nargs='*',
            help=(
            'A positional contents of a card'
            ))

    # TODO: LOCALE
    parser.add_argument(
            '-D', '--deck',
            action='store', dest='deck',
            help=(
            'Set a Deck.'
            ))

    # TODO: LOCALE
    parser.add_argument(
            '-t', '--type',
            action='store', dest='cardtype',
            help=(
            'Set a card type.'
            ))

    parser.add_argument(
            '-i', '--ip',
			# Do I need to remove it? Because of class parsed_config
            action='store', dest='ip',
            help=(
            'Set a AnkiConnect ip.'
            ))

    parser.add_argument(
            '-p', '--port',
			# Do I need to remove it? Because of class parsed_config
            action='store', dest='port', type=int,
            help=(
            'Set a AnkiConnect port.'
            ))

    parser.add_argument(
            '-f', '--file',
            action='store', dest='file', nargs='*',
            help=(
            'Set a file which contains card contents.'
            ))

    # ~/.acprc OR optional .acprc
    # parser.file: List
    # TODO : Execute configparse to a string object.
    parser.add_argument(
            '-c', '--config',
			metavar="file",
            action='store', dest='config',
            help=(
            "Set a config file to import options. Without this argument, this program uses '~/.asprc'"
            ))

    # get an alias from a config file.
    # looking for ~/.acprc OR ANKIADDERALL_CONFIG
    # TODO : Execute configparse to a string object.
    parser.add_argument(
            '--alias',
			metavar="section",
            action='store', dest='alias',
            help=(
            "Set a section of a config file to apply options. Without this argument, a default section is 'default'"
            ))

    parser.add_argument(
            '-F', '--IFS',
            action='store', dest='IFS',
            help=(
            "Set a delimiter of card contents to use any character other than a tab(\\t) character."
            ))

    parser.add_argument(
			# TODO: field?
            '--field',
            metavar="colon:delimiter-separated:fields",
			action='store', dest='field',
            help=(
            "Set an order of card field where you want to put separated strings. For example, the default is 'Front:Back:Tags'"
            ))

    parser.add_argument(
            '--cloze-field',
			metavar="colon:delimiter-separated:fields",
            action='store', dest='cloze_field',
            help=(
            "Set an order of card field where you want to put separated strings. For example, 'Text:tags'. The default is 'Text:Back Extra:Tags'"
            ))

    parser.add_argument(
            '--cloze-type',
            action='store', dest='cloze_type',
            help=(
            "Set a type of a fallback for a cloze type."
            ))

    parser.add_argument(
            '--toml-generate',
            action='store_true', dest='toml_generate',
            help=(
            "Print toml configs with current arguments. To set a section, use '--toml-section'"
            ))

    parser.add_argument(
            '--toml-write',
			metavar="file",
            action='store', dest='toml_write', 
            help=(
            "Write a toml file with options used. To set a section, use '--toml-section'"
            ))

    parser.add_argument(
            '--toml-section',
			metavar="section",
            action='store', dest='toml_section',
            help=(
            "Set a toml section. The default is 'untitled'"
            ))

    parser.add_argument(
            '-H', '--render-HTML',
            action='store_true', dest='allow_HTML',
            help=(
            "Set to allow to render a HTML tag. The default doesn't allow render a HTML tag"
            ))

    parser.add_argument(
            '--apikey',
            action='store', dest='apikey',
            help=(
            "Set an api key for AnkiConnect."
            ))

    parser.add_argument(
            '--sync',
            action='store_true', dest='sync',
            help=(
            "Sync Anki."
            ))

    parser.add_argument(
            '--force-add',
            action='store_true', dest='force_add',
            help=(
            "add a card even if there is a duplicate in the deck."
            ))

    parser.add_argument(
            '--dry-run',
            action='store_true', dest='dryrun',
            help=(
            'Perform a trial run without sending to Anki.'
            ))

    parser.add_argument(
            '-v', '--verbose',
            action='store_const', dest='verbose', const=logging.INFO,
            help=(
            'A verbose option.'
            ))

    parser.add_argument(
            '--debug',
            action='store_const', dest='debug', const=logging.DEBUG,
            help=(
            'A debug option'
            ))

    parser.add_argument(
            '-V', '--version',
            action='version', dest='version', version=VERSION,
            help=(
            'Print a version number and a license of trrc.'
            ))

    return parser
