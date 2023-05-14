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
  pourc --field 'ArbitraryFourthFieldName:ArbitrarysecondFieldName:tag' 'FourthContent\tsecondContent\ttag'
  pourc --ip 192.168.1.230 --port 4832 --debug --file Korean_English_conversation.txt
  # bash
  echo -e 'basic_type_front_normal_tab with option\\tbasic_type_back\\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --field 'Front:Back:tag' --debug
  # zsh
  echo 'basic_type_front_normal_tab with option\\tbasic_type_back\\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --field 'Front:Back:tag' --debug
  # supports HEREDOC
  pourc <<EOF --debug
  front	back	text
  EOF
"""

    parser = argparse.ArgumentParser(
            prog='pourc',
            description='a command line application to create anki cards',
            epilog=example_text,
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
            '--read-file-in-a-content',
            action='store_true', dest='contents_file_import',
            help=(
            "Set to allow to replace a file in contents with a file contents. a default setting doesn't read it"
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

    return parser
