import os
import sys
import tomlkit
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ankiadderall.create_parser import create_parser, parse_argument
from ankiadderall.ankiadderall import Regex_Pattern
from ankiadderall.configOpts import read_toml_config
from unittest import mock

@pytest.fixture
def regexes():
    return Regex_Pattern()

def test_ssparse_argument(capsys, monkeypatch):
    with mock.patch('sys.stdin') as stdin, mock.patch.object(sys, 'argv', ["program name", "front	back	test"] ):
        stdin.isatty.return_value = False
        test_case = """
front	back	test
2front	back	test
"""
        print(test_case)
        captured = capsys.readouterr()
        captured = [ x+'\n' for x in captured.out.split('\n')]

        assert type(captured) != type([])
        card_candidate, options = parse_argument()
        assert card_candidate == []

@pytest.mark.parametrize("mock_side_effect",
                         [None,
                          FileNotFoundError],)
@pytest.mark.parametrize("config_file_name",
                         [None, # the program looks for '~/.asprc'. it is a default.
                          'some_random.asprc']) # user uses arbitrary config file.
@pytest.mark.parametrize("user_section", # user uses argparse option alias.
                         ['NoSuchASection', # user places wrong section name in argparse option
                          None, # user doesn't use argparse option. It uses default as a hardcoded setting.
                          'default'])
@pytest.mark.parametrize("section_in_file",
                         ['default',
                          'arbitrary'],)
def test_read_toml_config(config_file_name, user_section, mock_side_effect, section_in_file):
    # TODO: read_data as a parametrize
    CASE_DATA_TO_READ = f'[{section_in_file}]\n' + """
    deck = "Linux::algo"
    cardtype = "Basic"
    ip = "127.0.0.1"
    port = 8765
    IFS = "	"
    apikey = "weirdankiconnectkey"
    contents_file_import = true
    column = "front:back:tag"
    cloze_field = "Text:Back Extra:tags"
    """

    with mock.patch("builtins.open", mock.mock_open(read_data=CASE_DATA_TO_READ)) as mock_file :
        mock_file.side_effect=mock_side_effect

        # if there is a file and user set an arbitrary section.
        if CASE_DATA_TO_READ and user_section in ['default','arbitrary'] and mock_side_effect is None:
            from tomlkit import loads
            toml_load = loads(CASE_DATA_TO_READ)

            if section_in_file == 'arbitrary' and user_section != 'arbitrary':
                assert read_toml_config(config_file_name, user_section) == {}
            else:
                assert read_toml_config(config_file_name, user_section) == toml_load[user_section]

        # If a config file exists and user doesn't set a section, then use a
        # 'default' section.
        elif CASE_DATA_TO_READ and user_section is None and mock_side_effect is None: 
            from tomlkit import loads
            toml_load = loads(CASE_DATA_TO_READ)
            hardcoded_section = 'default'
            if section_in_file == 'arbitrary' and user_section != 'arbitrary':
                #with pytest.raises(Exception) as e:
                assert read_toml_config(config_file_name, user_section) == {}
            else:
                assert read_toml_config(config_file_name, user_section) == toml_load[hardcoded_section]
        elif mock_side_effect is FileNotFoundError and config_file_name is not None:
            with pytest.raises(SystemExit) as e:
                read_toml_config(config_file_name, user_section)
        else:
            assert read_toml_config(config_file_name, user_section) == {}
