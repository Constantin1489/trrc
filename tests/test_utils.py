import os
import sys
import tomlkit
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trrc.create_parser import create_parser, parse_argument
import trrc.utils as utils
from trrc.utils import RegexPattern
from trrc.config_opts import read_toml_config
from unittest import mock

@pytest.fixture
def regex_compiles():
    regex = RegexPattern()
    return regex

@pytest.mark.parametrize("card_str, br_answer, prevent_HTML_answer",
                         [('long <br>sent\\nences\\\\n', 'long <br>sent<br>ences&#92n', 'long &ltbr&gtsent\\nences\\\\n'),
                          ('other <br>sent\\nences\\\\n', 'other <br>sent<br>ences&#92n', 'other &ltbr&gtsent\\nences\\\\n')])
def test_regexes_compiles(regex_compiles, card_str, br_answer, prevent_HTML_answer):

    re_compile = regex_compiles.newline_to_html_br_compile
    pattern = regex_compiles.newline_to_html_br_pattern

    assert re_compile.sub(lambda mo: pattern[mo.group()], card_str) == br_answer

    re_compile = regex_compiles.prevent_html_interpret_compile
    pattern = regex_compiles.prevent_html_interpret_pattern

    assert re_compile.sub(lambda mo: pattern[mo.group()], card_str) == prevent_HTML_answer

@pytest.mark.parametrize("mock_side_effect",
                         [None,
                          FileNotFoundError],)
@pytest.mark.parametrize("config_file_name",
                         [None, # the program looks for '~/.trrc'. it is a default.
                          'some_random.trrc']) # user uses arbitrary config file.
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
        if user_section in ['NoSuchASection', 'default'] and mock_side_effect is None:
            from tomlkit import loads
            toml_load = loads(CASE_DATA_TO_READ)

            if section_in_file != user_section:
                with pytest.raises(KeyError) as e:
                    read_toml_config(config_file_name, user_section)

            else:
                assert read_toml_config(config_file_name, user_section) == toml_load[user_section]

        # If a config file exists and user doesn't set a section, then use a
        # 'default' section.
        elif user_section is None and mock_side_effect is None:
            from tomlkit import loads
            toml_load = loads(CASE_DATA_TO_READ)
            hardcoded_section = 'default'
            if section_in_file == 'arbitrary':
                with pytest.raises(KeyError) as e:
                    read_toml_config(config_file_name, user_section)

            else:
                assert read_toml_config(config_file_name, user_section) == toml_load[hardcoded_section]
        elif mock_side_effect is FileNotFoundError and config_file_name is not None:
            with pytest.raises(SystemExit) as e:
                read_toml_config(config_file_name, user_section)
        else:
            assert read_toml_config(config_file_name, user_section) == {}

def test_utils_card_class_WRONG_IFS(capsys):
    WRONGIFS = '#'
    temp_card_obj = utils.Card('default', 'basic', 'front%back%test',
                               'front:back:tags', None, None, WRONGIFS)
    temp_card_obj.make_card()
    capture = capsys.readouterr()
    assert capture.err[0:5] == 'ERROR'

@pytest.mark.parametrize("cardcontents, IFS_in_str",
                         [('front%back%test', '%'),
                          ('front	back	test second_tag', '\t'),
                          ('front	back	test', '\t'),
                          ('front\tback\ttest', '\t')],)
@pytest.mark.parametrize("deckname", ['default', 'arbitrary name'])
@pytest.mark.parametrize("cardtype", ['basic', 'deck name with space', 'cloze']) # there can be a cloze but I should not raise an error in this phase. AnkiConnect will report an error.
@pytest.mark.parametrize("field", ['front:back:tags', 'back:front:tags'])
def test_utils_card_class_correct_IFS(capsys, IFS_in_str, deckname,
                                      cardcontents, cardtype, field):
    temp_card_obj = utils.Card(deckname, cardtype, cardcontents, field, None,
                               None, IFS_in_str)

    content_answer = dict(zip(field.split(sep=':') , cardcontents.split(sep=IFS_in_str)))
    tag = content_answer.pop('tags').split(sep=' ')

    temp_card_obj.make_card()
    capture = capsys.readouterr()
    assert capture.err == ''
    assert capture.out == ''
    assert vars(temp_card_obj)['content'] == content_answer
    assert vars(temp_card_obj)['tag'] == tag
    assert temp_card_obj.create_cardjson_note() == {'deckName': deckname,
                                                    'fields': content_answer,
                                                    'modelName': cardtype,
                                                    'tags': tag}

@pytest.mark.parametrize("cardcontents, IFS_in_str",
                         [('front%back%test', '%'),
                          ('front	back	test second_tag', '\t'),
                          ('front	back	test', '\t'),
                          ('front\tback\ttest', '\t')],)
@pytest.mark.parametrize("deckname", ['default', 'arbitrary name'])
@pytest.mark.parametrize("cardtype", ['basic', 'deck name with space', 'cloze']) # there can be a cloze but I should not raise an error in this phase. AnkiConnect will report an error.
def test_utils_card_class_correct_IFS_None_user_field(capsys, IFS_in_str, deckname,
                                                             cardcontents, cardtype):
    temp_card_obj = utils.Card(deckname, cardtype, cardcontents, None, None,
                               None, IFS_in_str)

    content_answer = dict(zip(['Front', 'Back', 'tags'], cardcontents.split(sep=IFS_in_str)))
    tag = content_answer.pop('tags').split(sep=' ')

    temp_card_obj.make_card()
    capture = capsys.readouterr()
    if cardtype == 'basic':
        assert capture.err == ''
        assert capture.out == ''
    assert vars(temp_card_obj)['content'] == content_answer
    assert vars(temp_card_obj)['tag'] == tag
    assert temp_card_obj.create_cardjson_note() == {'deckName': deckname,
                                                     'fields': content_answer,
                                                     'modelName': cardtype,
                                                     'tags': tag}

@pytest.mark.parametrize("deckname", ['default', 'arbitrary name'])
@pytest.mark.parametrize("cardcontents, IFS_in_str",
                         [('fr{{c1::o}}nt%back%test', '%'),
                          ('fr{{c1::o}}nt	back	test', '\t'),
                          ('fr{{c1::o}}nt	back	test second_tag', '\t'),
                          ('fr{{c1::o}}nt\tback\ttest', '\t')],)
@pytest.mark.parametrize("field", ['Back Extra:Text:tags', 'Text:Back Extra:tags'])
def test_utils_card_class_cloze(capsys, IFS_in_str, cardcontents, deckname, field):
    temp_card_obj = utils.Card(deckname, 'cloze', cardcontents, field, None,
                               None, IFS_in_str)

    content_answer = dict(zip(field.split(sep=':') , cardcontents.split(sep=IFS_in_str)))
    tag = content_answer.pop('tags').split(sep=' ')

    temp_card_obj.make_card()
    capture = capsys.readouterr()
    assert capture.err == ''
    assert capture.out == ''
    assert vars(temp_card_obj)['content'] == content_answer
    assert vars(temp_card_obj)['tag'] == tag
    assert temp_card_obj.create_cardjson_note() == {'deckName': deckname,
                                                    'fields': content_answer,
                                                    'modelName': 'cloze',
                                                    'tags': tag}

@pytest.mark.parametrize("deckname", ['default', 'arbitrary name'])
@pytest.mark.parametrize("cardcontents, IFS_in_str",
                         [('fr{{c1::o}}nt%back%test', '%'),
                          ('fr{{c1::o}}nt	back	test', '\t'),
                          ('fr{{c1::o}}nt	back	test second_tag', '\t'),
                          ('fr{{c1::o}}nt\tback\ttest', '\t')],)
def test_utils_card_class_cloze_None_user_field(capsys, IFS_in_str, cardcontents, deckname):
    temp_card_obj = utils.Card(deckname, 'cloze', cardcontents, None, None,
                               None, IFS_in_str)

    content_answer = dict(zip(['Text', 'Back Extra', 'tags'], cardcontents.split(sep=IFS_in_str)))
    tag = content_answer.pop('tags').split(sep=' ')

    temp_card_obj.make_card()
    capture = capsys.readouterr()
    assert capture.err == ''
    assert capture.out == ''
    assert vars(temp_card_obj)['content'] == content_answer
    assert vars(temp_card_obj)['tag'] == tag
    assert temp_card_obj.create_cardjson_note() == {'deckName': deckname,
                                                    'fields': content_answer,
                                                    'modelName': 'cloze',
                                                    'tags': tag}
