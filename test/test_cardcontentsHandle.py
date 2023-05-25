import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trrc.create_parser import create_parser, parse_argument
import configparser
# create_parser.create_parser


@pytest.fixture
def parser():
    return create_parser()


def test_port_option(parser):
    """
    Test a port option
    """

    # a short port option
    result = parser.parse_args('-p 30 some'.split())
    assert  result.port == 30

    # a long port option
    result = parser.parse_args('--port 30 some'.split())
    assert  result.port == 30

    # a default port option
    # if there is no argument in parse_args(), then pytest --tb=line raise
    # error.
    result = parser.parse_args([])
    assert  result.port == None


def test_file_option(parser):
    """
    Test a file input option
    """

    thisFile = os.path.abspath(__file__)

    # a short file option for a empty input
    result = parser.parse_args(f'--port 30'.split())
    assert type(result.file) == type(None)

    # a short file option
    result = parser.parse_args(f'-f {thisFile}'.split())
    assert result.file == [os.path.abspath(__file__)]

    # a long file option
    result = parser.parse_args(f'--file {os.path.abspath(__file__)}'.split())
    assert result.file == [os.path.abspath(__file__)]

    # check whether is a list
    assert type(result.file) == type([])

    # multiple files option
    result = parser.parse_args(f'--file {os.path.abspath(__file__)} {os.path.abspath(__file__)}'.split())
    assert result.file == [os.path.abspath(__file__), os.path.abspath(__file__)]

def test_IFS_option(parser):
    """
    Test a IFS option
    """

    result = parser.parse_args(f"-F 'x'".split())

    assert result.ifs == "'x'"
    assert len(result.ifs) == 3

    result = parser.parse_args(f"-F x".split())
    assert result.ifs == 'x'
    assert len(result.ifs) == 1

    result = parser.parse_args(f"--IFS x".split())
    assert result.ifs == 'x'
    assert len(result.ifs) == 1

def test_card_deck(parser):
    """
    Test a card deck.
    """

    testdeck = 'linux::algo'

    # test a default deck value.
    # To get a default deck value, put an arbitrary argument with a valid option.
    result = parser.parse_args(f'-F x'.split())
    assert result.deck == None

    # a short deck option with an arbitrary test deck.
    result = parser.parse_args(f'-D {testdeck}'.split())
    assert result.deck == 'linux::algo'

    # a long deck option with an arbitrary test deck.
    result = parser.parse_args(f'--deck {testdeck}'.split())
    assert result.deck == 'linux::algo'
    result = parser.parse_args(f'--deck {testdeck} second'.split())
    assert result.deck == 'linux::algo'

def test_parse_multiple_option(parser):
    """

    :parser: TODO
    :returns: TODO

    """

    result = parser.parse_args(f'/Users/constantinhong/TODO/tempfile_dir/snippet.q2iIDLVU.ExportedCard -p 8888 -F x'.split())
    assert result.port == 8888
    assert result.ifs == 'x'
    assert result.cardContents == ['/Users/constantinhong/TODO/tempfile_dir/snippet.q2iIDLVU.ExportedCard' ]
    assert result.file == None

def test_card_type(parser):
    """
    Test a card type.
    """

    testCardType = 'cloze123'

    # test a default deck value.
    # To get a default deck value, put an arbitrary argument with a valid option.
    result = parser.parse_args(f'-F x'.split())
    assert result.cardtype == None

    # a short file option with an arbitrary test deck.
    result = parser.parse_args(f'-t {testCardType}'.split())
    assert result.cardtype == testCardType

    # a long file option with an arbitrary test deck.
    result = parser.parse_args(f'--type {testCardType}'.split())
    assert result.cardtype == testCardType

#def test_parse_argument():
#    """
#    Test a parse_argument function
#    :returns: TODO
#
#    """
#    arg = 'front	back	vim'
#    
#    # TODO
#    assert parse_argument(['program',arg]) == ''

@pytest.mark.parametrize("stdin_arg, debug_value",
                         [['--debug', 10],
                          ['', None]])
def test_debug_option(parser, stdin_arg, debug_value):
    """
    Test a debug option
    """

    result = parser.parse_args(stdin_arg.split())
    assert  result.debug == debug_value

@pytest.mark.parametrize("stdin_arg, verbose_value",
                         [['--verbose', 20],
                          ['', None]])
def test_verbose_option(parser, stdin_arg, verbose_value):
    """
    Test a verbose option
    """

    result = parser.parse_args(stdin_arg.split())
    assert  result.verbose == verbose_value
