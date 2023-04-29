import argparse
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_parser():
    """
    create_parser
    """

	# TODO: Do not remove.
    example_text="""
[example]
  pourc '안녕	Hello	Korean Conversation'
  pourc $'안녕\\tHello\\tKorean'
  pourc "back\\ttestfront\\tvim" -F '\\t'
  pourc --IFS % '안녕%Hello%Korean'
  pourc --column 'ArbitraryFourthFieldName:ArbitrarysecondFieldName:tag' 'FourthContent\tsecondContent\ttag'
  pourc --ip 192.168.1.230 --port 4832 --debug --file Korean_English_conversation.txt
  # bash
  echo -e 'basic_type_front_normal_tab with option\\tbasic_type_back\\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug
  # zsh
  echo 'basic_type_front_normal_tab with option\\tbasic_type_back\\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug
"""

    parser = argparse.ArgumentParser(
            prog='pourc',
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
			# Do I need to remove it? Because of class parsed_config
            action='store', dest='ip',
            help=(
            'set a AnkiConnect ip.'
            ))

    parser.add_argument(
            '-p', '--port',
			# Do I need to remove it? Because of class parsed_config
            action='store', dest='port', type=int,
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
            'Use options of an alias of a config file'
            ))

    parser.add_argument(
            '-F', '--IFS',
            action='store', dest='IFS',
            help=(
            "a delimiter of card contents. To use other than a tab character, use this option."
            ))

    parser.add_argument(
			# TODO: field?
            '--column', action='store', dest='column', nargs='?',
            type=lambda s: [i for i in s.split(':')],
            help=(
            'Set an order of card field where you want to put separated strings.'
            ))

    parser.add_argument(
            '--toml-generate',
            action='store_true', dest='toml_generate',
            help=(
            'Print the cards that would be created and options that would be applied, but do not execute the command.'
            ))

    parser.add_argument(
            '--toml-write',
            action='store', dest='toml_write', 
            help=(
            'Print the cards that would be created and options that would be applied, but do not execute the command.'
            ))

    parser.add_argument(
            '--toml-section',
            action='store', dest='toml_section',
            #action='store', dest='toml_section', default='untitled',
            help=(
            'Print the cards that would be created and options that would be applied, but do not execute the command.'
            ))

    parser.add_argument(
            '--dry-run',
            action='store_true', dest='dryrun',
            help=(
            'Print the cards that would be created and options that would be applied, but do not execute the command.'
            ))

    parser.add_argument(
            '-v', '--verbose',
            action='store_const', dest='verbose', const=logging.INFO,
            help=(
            'a verbose option'
            ))

    parser.add_argument(
            '--debug',
            action='store_const', dest='debug', const=logging.DEBUG,
            help=(
            'a debug option'
            ))

    return parser
