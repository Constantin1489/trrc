import sys
import os
import io
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trrc.create_parser import parse_argument

# test for a file piping
basic_and_cloze = """
mix_basic_type_front_cat1 basic_type_back test_tag
cloze {{c1::asdfasdfas::}}    asdfklasj   test_tag 

#comment to be ignored
mix_basic_type_front_cat2 basic_type_back test_tag
"""
file_with_string_and_empty_string = """
before_empty_line_basic_type_front_cat1    basic_type_back test_tag

after_empty_line_basic_type_front_cat2 basic_type_back test_tag
"""

file_with_only_empty_string = """
"""

file_with_basics_and_comments = """
basic_type_front_cat1  basic_type_back test_tag
#comment to be ignored
basic_type_front_cat2  basic_type_back test_tag
"""

file_with_sole_cloze = """
Here, {{c1::__init__()::}} is the constructor function that is called whenever a new object of that class is instantiated.     test_tag
"""

oneline_echo_pipe_parametor = pytest.mark.parametrize("user_input", ['front\tback\ttag', 'front\tback\ttag\n\nfront2\tback\ttag'])
cat_file_pipe_parametor = pytest.mark.parametrize("user_input", [basic_and_cloze, file_with_string_and_empty_string, file_with_only_empty_string, file_with_basics_and_comments, file_with_sole_cloze])
stdin_parametor = pytest.mark.parametrize("user_input", ['front\tback\ttag', 'front\tback\ttag\n\nfront2\tback\ttag'])

@oneline_echo_pipe_parametor
def test_parse_argument_pipe_redirection(capsys, monkeypatch, user_input):
    monkeypatch.setattr('sys.stdin', io.StringIO(user_input))
    card_candidate, options = parse_argument()
    answer = user_input.split(sep='\n')
    assert card_candidate == answer

@cat_file_pipe_parametor
def test_parse_argument_pipe_redirection(capsys, monkeypatch, user_input):
    monkeypatch.setattr('sys.stdin', io.StringIO(user_input))
    card_candidate, options = parse_argument()
    card_candidate.append('')

    answer = []
    for card in  user_input.split(sep='\n'):
            card = card + '\n'
            if card[0] == '#':
                continue

            parsed_a_line = card.rstrip('\n')
            answer.append(parsed_a_line)

    assert card_candidate == answer

@stdin_parametor
def test_parse_argument_stdin(monkeypatch, user_input):
    monkeypatch.setattr('sys.stdin.isatty', (lambda: True))

    answer = user_input.split(sep='\n')
    user_input_split = user_input.split(sep='\n')

    card_candidate, options = parse_argument(user_input_split)
    # TODO: multiple cards in stdin test
    assert card_candidate == answer




def test_parse_argument_stdin_multiple_inputs(monkeypatch):
    monkeypatch.setattr('sys.stdin.isatty', (lambda: True))

    # example
    #$ pourc 'front\tback\ttag' '' 'front2\tback\ttag'
    user_input = "'front	back	test' '' 'front2	back	test'"
    answer = user_input.split(sep='\n')
    user_input_split = user_input.split(sep='\n')

    card_candidate, options = parse_argument(user_input_split)
    assert card_candidate == answer
