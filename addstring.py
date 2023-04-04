#!/usr/bin/env python
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
    sys.exit(main())
