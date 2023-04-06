#!/usr/bin/env python
import pytest
import sys


class pipe_redirection:
    tests = [
        'something\tsadfas\tasdknfas',
        '1something\tsadfas\tasdknfas',
        '14mix_basic_type_front_cat1	basic_type_back	basic_type_tag',
        '15cloze {{c1::asdfasdfas::}}	asdfklasj	test cloze',
        '16mix_basic_type_front_cat2	basic_type_back	basic_type_tag',
        'fourRow' + '\tfourRow' * 3,
    ]

def make_test(StringToTest):
    return {'test': StringToTest, 'answer': StringToTest + '\n'}

def test_pipe_redirection(capsys):
    
    for test in pipe_redirection.tests:

        test = make_test(test)
        print(test['test'])
        captured = capsys.readouterr()

        assert captured.out == test['answer']
