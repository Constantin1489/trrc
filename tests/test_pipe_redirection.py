#!/usr/bin/env python
import pytest
import sys

def make_test(test_case):
    return {'test': test_case, 'answer': test_case + '\n'}

@pytest.mark.parametrize("string_test_case",
                         [ 'something\tsadfas\tasdknfas',
                          '1something\tsadfas\tasdknfas',
                          '14mix_basic_type_front_cat1	basic_type_back	basic_type_tag',
                          '15cloze {{c1::asdfasdfas::j}	asdfklasj	test cloze',
                          '16mix_basic_type_front_cat2	basic_type_back	basic_type_tag',
                          'fourRow' + '\tfourRow' * 3 ])
def test_pipe_redirection(string_test_case, capsys):
    
    test = make_test(string_test_case)
    print(test['test'])
    captured = capsys.readouterr()

    assert captured.out == test['answer']
