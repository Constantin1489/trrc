import sys
import os
import io
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ankiadderall.ankiadderall as ankiadderall
from ankiadderall.create_parser import parse_argument

parametor = pytest.mark.parametrize("user_input", ['front\tback\ttag', 'front\tback\ttag\n\nfront2\tback\ttag'])

@parametor
def test_parse_argument_pipe_redirection(capsys, monkeypatch, user_input):
    monkeypatch.setattr('sys.stdin', io.StringIO(user_input))
    card_candidate, options = parse_argument()
    answer = user_input.split(sep='\n')
    assert card_candidate == answer

@parametor
def test_parse_argument_stdin(monkeypatch, user_input):
    monkeypatch.setattr('sys.stdin.isatty', (lambda: True))

    #$ pourc 'front\tback\ttag' '' 'front2\tback\ttag'
    answer = user_input.split(sep='\n')
    user_input_split = user_input.split(sep='\n')

    card_candidate, options = parse_argument(user_input_split)
    assert card_candidate == answer
