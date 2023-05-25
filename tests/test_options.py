import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trrc.create_parser import create_parser, parse_argument
from trrc.config_opts import ParsedConfig, toml_arg_handle, make_toml, mask_apikey
import tomli_w

@pytest.fixture
def parser():
    return create_parser()

@pytest.fixture
def empty_parsed_arg(parser):
    return parser.parse_args([])

def test_option_initialization(empty_parsed_arg):
    options = ParsedConfig(empty_parsed_arg)
    assert vars(options).keys() == vars(empty_parsed_arg).keys()

@pytest.mark.parametrize("sysargv_toml_case, answer", [(['--toml-generate' ],
                                                        True), ([], False)])
def test_toml_generate(parser, sysargv_toml_case, answer):

    parsed_arg = parser.parse_args(sysargv_toml_case)
    assert parsed_arg.toml_generate == answer
    assert parsed_arg.toml_generate or parsed_arg.toml_write == ( answer or None)

@pytest.mark.parametrize("do_print_toml, do_print_toml_answer",
                         [(False, False),
                          (True, True)])
@pytest.mark.parametrize("config_file_name, config_file_name_answer",
                         [(None, None),
                          ('new.trrc', 'new.trrc'),])
@pytest.mark.parametrize("section_title, section_title_answer",
                         [(None, 'untitled'),
                          ('untitled', 'untitled'),
                          ('new_section_title', 'new_section_title')])
def test_toml_arg_handle(capsys, empty_parsed_arg, do_print_toml,
                         do_print_toml_answer, config_file_name,
                         config_file_name_answer, section_title,
                         section_title_answer):
    """TODO: Docstring for toml_arg_handle.

    :arg1: TODO
    :returns: TODO

    """
    parsed_arg = vars(empty_parsed_arg)

    if not do_print_toml and not config_file_name:
        pytest.skip('Cannot happen')

    with pytest.raises(SystemExit) as e:
        toml_arg_handle(do_print_toml, config_file_name, section_title, parsed_arg)

    assert e.type == SystemExit
    assert e.value.code == 2

    captured = capsys.readouterr()

    if do_print_toml:
        section_title = 'untitled' if not section_title else section_title
        toml_answer_set = make_toml(parsed_arg, section_title)
        toml_answer_set = tomli_w.dumps(toml_answer_set)
        assert captured.out == toml_answer_set + '\n'

@pytest.mark.parametrize("apikey, masked_string",
                         [(None, None),
                          ('WeirdLongString', 'masked')],)
def test_mask_apikey(parser, apikey, masked_string):
    parsed_arg = parser.parse_args(['--apikey', apikey ])
    assert mask_apikey(vars(parsed_arg))["apikey"] == masked_string
