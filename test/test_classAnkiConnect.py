import sys
import re
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ankiadderall.ankiadderall as ankiadderall
import argparse

def test_get_default_get_AnkiConnect_URL():
    assert ankiadderall.userAnkiConnect() == 'http://localhost:8765'
    assert ankiadderall.userAnkiConnect('0.0.0.0', 132) == 'http://0.0.0.0:132'
    assert ankiadderall.userAnkiConnect('0.0.0.0', 132) != '0.0.0.0'
    assert ankiadderall.userAnkiConnect('personalWeb.com', 132) == 'http://personalWeb.com:132'
    assert ankiadderall.userAnkiConnect('https://personalWeb.com', 132) == 'https://personalWeb.com:132'
