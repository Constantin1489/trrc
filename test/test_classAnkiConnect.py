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
    assert ankiadderall.userAnkiConnect() == 'http://localhost:8765'
    assert ankiadderall.userAnkiConnect('0.0.0.0', 132) == 'http://0.0.0.0:132'
    assert ankiadderall.userAnkiConnect('0.0.0.0', 132) != '0.0.0.0'
