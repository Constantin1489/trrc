import sys
import re
import os
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiadderall')
import ankiadderall
import argparse

userAnkico = ankiadderall.userAnkiConnect('asdfasdf', 132)
#assert userAnkico._webBindAddress == 
#assert userAnkico._webBindPort == 
#assert userAnkico.returnURL() == 
#assert ankiadderall.userAnkiConnect('0.0.0.0', 132).returnURL() == 
#assert ankiadderall.userAnkiConnect('0.0.0.0', 132)._webBindAddress == 
#print('default', ankiadderall.userAnkiConnect().returnURL())
def test_get_default_get_AnkiConnect_URL():
    assert ankiadderall.userAnkiConnect().get_AnkiConnect_URL() == 'localhost:8765'
    assert userAnkico._webBindAddress == 'asdfasdf'
    assert userAnkico._webBindPort == 132
    assert userAnkico.get_AnkiConnect_URL() == 'asdfasdf:132'
    assert ankiadderall.userAnkiConnect('0.0.0.0', 132).get_AnkiConnect_URL() == '0.0.0.0:132'
    assert ankiadderall.userAnkiConnect('0.0.0.0', 132)._webBindAddress == '0.0.0.0'

