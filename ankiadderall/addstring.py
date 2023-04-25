#!/usr/bin/env python
import sys
import re
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ankiadderall.create_parser import parse_argument, parse_card

def main():

    card_candidate, options = parse_argument()
    parse_card(card_candidate, options)

if __name__ == '__main__' :
    sys.exit(main())
