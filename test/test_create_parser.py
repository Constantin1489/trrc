import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# create_parser.create_parser

def test_create_parser():
    """
    Test a port option
    """

    parser = create_parser()

    # a short port option
    result = parser.parse_args('-p 30 some'.split())
    assert  result.port == 30

    # a long port option
    result = parser.parse_args('--port 30 some'.split())
    assert  result.port == 30

    # a default port option
    result = parser.parse_args()
    assert  result.port == 8765


def test_file_option():
    """
    Test a file input option
    """
    parser = create_parser()
    thisFile = os.path.abspath(__file__)

    # a short file option
    result = parser.parse_args(f'-f {thisFile}'.split())
    assert result.file == [os.path.abspath(__file__)]
    # TODO : Do I need this?
    assert os.path.isfile(*result.file) == True

    # a long file option
    result = parser.parse_args(f'--file {os.path.abspath(__file__)}'.split())
    assert result.file == [os.path.abspath(__file__)]

    # multiple files option
    result = parser.parse_args(f'--file {os.path.abspath(__file__)} {os.path.abspath(__file__)}'.split())
    assert result.file == [os.path.abspath(__file__), os.path.abspath(__file__)]

def test_IFS_option():
    """
    Test a IFS option
    """

    parser = create_parser()
    result = parser.parse_args(f"-F 'x'".split())

    assert result.IFS == "'x'"
    assert len(result.IFS) == 3

    result = parser.parse_args(f"-F x".split())
    assert result.IFS == 'x'
    assert len(result.IFS) == 1

def test_card_deck():
    """
    Test a card deck.
    """

    parser = create_parser()
    testdeck = 'linux::algo'

    # test a default deck value.
    # To get a default deck value, put an arbitrary argument with a valid option.
    result = parser.parse_args(f'-F x'.split())
    assert result.deck == 'Default'

    # a short file option with an arbitrary test deck.
    result = parser.parse_args(f'-D {testdeck}'.split())
    assert result.deck == 'linux::algo'

    # a long file option with an arbitrary test deck.
    result = parser.parse_args(f'--deck {testdeck}'.split())
    assert result.deck == 'linux::algo'

def test_card_type():
    """
    Test a card type.
    """

    parser = create_parser()
    testCardType = 'cloze123'

    # test a default deck value.
    # To get a default deck value, put an arbitrary argument with a valid option.
    result = parser.parse_args(f'-F x'.split())
    assert result.cardtype == 'basic'

    # a short file option with an arbitrary test deck.
    result = parser.parse_args(f'-D {testCardType}'.split())
    assert result.deck == testCardType

    # a long file option with an arbitrary test deck.
    result = parser.parse_args(f'--deck {testCardType}'.split())
    assert result.deck == testCardType
