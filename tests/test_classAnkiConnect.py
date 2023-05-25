import sys
import re
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import trrc.utils as ankiadderall
import argparse

def test_get_default_get_ankiconnect_url():
    assert ankiadderall.get_user_ankiconnect() == 'http://localhost:8765'
    assert ankiadderall.get_user_ankiconnect('0.0.0.0', 132) == 'http://0.0.0.0:132'
    assert ankiadderall.get_user_ankiconnect('0.0.0.0', 132) != '0.0.0.0'
    assert ankiadderall.get_user_ankiconnect('personalWeb.com', 132) == 'http://personalWeb.com:132'
    assert ankiadderall.get_user_ankiconnect('https://personalWeb.com', 132) == 'https://personalWeb.com:132'
