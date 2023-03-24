#!/usr/local/bin/python

import sys
import re
import os
from options import parse_argument, parse_card

def makeParser():
    pass


if __name__ == '__main__' :

    ANKIADDERALL_CONFIG = { 'DECK': 'Linux', 'TYPE':'Basic'  }

    # assign a card deck.
    # seek the shell env variable. if it doesn't exist, then use a compiled DECK value.
    # let's just get all environment value and check all.
    # if deck and type is not configed then use Anki program default Deck and card type setting.
    DECK = os.environ['ANKIADDERALL_DECK'] if 'ANKIADDERALL_DECK' in os.environ.keys() else ANKIADDERALL_CONFIG['DECK']
    TYPE = os.environ['ANKIADDERALL_TYPE'] if 'ANKIADDERALL_TYPE' in os.environ.keys() else ANKIADDERALL_CONFIG['TYPE']

    card_candidate = parse_argument(sys.argv)
    parse_card(card_candidate, DECK, TYPE)
    exit(0)
