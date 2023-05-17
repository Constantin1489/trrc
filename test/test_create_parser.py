import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ankiadderall.create_parser import gather_card_from
from ankiadderall.ankiadderall import Regex_Pattern
import ankiadderall.ankiadderall as ankiadderall

@pytest.fixture
def regexes_compiles():
    regexes = Regex_Pattern()
    return regexes

def test_ankiadderall_card_class_WRONG_IFS(capsys):
    WRONGIFS = '#'
    tempCardObject = ankiadderall.card('default',
                                       'basic',
                                       'front%back%test',
                                       'front:back:tags',
                                       None,
                                       None,
                                       WRONGIFS)
    tempCardObject.make_card()
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
def test_ankiadderall_card_class_correct_IFS(capsys, IFS_in_str, deckname,
                                             cardcontents, cardtype, field):
    tempCardObject = ankiadderall.card(deckname,
                                       cardtype,
                                       cardcontents,
                                       field,
                                       None,
                                       None,
                                       IFS_in_str)

    content_answer = dict(zip(field.split(sep=':') , cardcontents.split(sep=IFS_in_str)))
    tag = content_answer.pop('tags').split(sep=' ')

    tempCardObject.make_card()
    capture = capsys.readouterr()
    assert capture.err == ''
    assert capture.out == ''
    assert vars(tempCardObject)['content'] == content_answer
    assert vars(tempCardObject)['tag'] == tag
    assert tempCardObject.create_cardjson_note() == {'deckName': deckname,
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
def test_ankiadderall_card_class_cloze(capsys, IFS_in_str, cardcontents, deckname, field):
    tempCardObject = ankiadderall.card(deckname,
                                       'cloze',
                                       cardcontents,
                                       field,
                                       None,
                                       None,
                                       IFS_in_str)

    content_answer = dict(zip(field.split(sep=':') , cardcontents.split(sep=IFS_in_str)))
    tag = content_answer.pop('tags').split(sep=' ')

    tempCardObject.make_card()
    capture = capsys.readouterr()
    assert capture.err == ''
    assert capture.out == ''
    assert vars(tempCardObject)['content'] == content_answer
    assert vars(tempCardObject)['tag'] == tag
    assert tempCardObject.create_cardjson_note() == {'deckName': deckname,
                                                     'fields': content_answer,
                                                     'modelName': 'cloze',
                                                     'tags': tag}
