#!/usr/local/bin/python

import sys
import re
import os
from create_parser import parse_argument, parse_card

def makeParser():
    pass

def main():

    card_candidate: List[parser] = parse_argument()
    parse_card(card_candidate)

if __name__ == '__main__' :


    # assign a card deck.
    # seek the shell env variable. if it doesn't exist, then use a compiled DECK value.
    # let's just get all environment value and check all.
    # if deck and type is not configed then use Anki program default Deck and card type setting.
    sys.exit(main())
