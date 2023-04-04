import argparse
import logging

parser = argparse.ArgumentParser(
        prog='Ankiadderall',
        description='a command line application to create anki cards',
        epilog='Constantin Hong'
        )

parser.add_argument(
        'cardContents', action='store', nargs='?',
        help=(
        'a positional contents of a card'
        ))

# TODO: fix default
# TODO: LOCALE
parser.add_argument(
        '-D', '--deck',
        action='store', dest='deck',
        help=(
        'set a Deck.'
        ))

# TODO: fix default
# TODO: LOCALE
parser.add_argument(
        '-t', '--type',
        action='store', dest='cardtype',
        help=(
        'set a card type.'
        ))

# TODO:
parser.add_argument(
        '-i', '--ip',
        action='store', dest='ip', default='127.0.0.1',
        help=(
        'set a AnkiConnect ip.'
        ))

# TODO:
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

# TODO:
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
        '--debug',
        action='store_const', dest='debug', const=logging.DEBUG,
        help=(
        'a debug option'
        ))
