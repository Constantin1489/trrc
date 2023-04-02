import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from create_parser import create_parser, parse_argument
# create_parser.create_parser


@pytest.fixture
def parser():
    return create_parser()


def test_create_parser(parser):
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
    result = parser.parse_args()
    assert  result.port == 8765


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

    # check whether is a list
    assert type(result.file) == type([])
    # TODO : Do I need this?
    assert os.path.isfile(*result.file) == True

    # a long file option
    result = parser.parse_args(f'--file {os.path.abspath(__file__)}'.split())
    assert result.file == [os.path.abspath(__file__)]

    # multiple files option
    result = parser.parse_args(f'--file {os.path.abspath(__file__)} {os.path.abspath(__file__)}'.split())
    assert result.file == [os.path.abspath(__file__), os.path.abspath(__file__)]

def test_IFS_option(parser):
    """
    Test a IFS option
    """

    result = parser.parse_args(f"-F 'x'".split())

    assert result.IFS == "'x'"
    assert len(result.IFS) == 3

    result = parser.parse_args(f"-F x".split())
    assert result.IFS == 'x'
    assert len(result.IFS) == 1

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

def test_debug_option(parser):
    """
    Test a debug-on option
    """

    result = parser.parse_args('--debug'.split())
    assert  result.debug == 10

def test_debug_option_off(parser):
    """
    Test a debug-off option
    """

    result = parser.parse_args(''.split())
    assert  result.debug == None
