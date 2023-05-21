#!/usr/bin/env python
import sys
import os
from .create_parser import parse_argument, parse_card

def main():

    card_candidate, options = parse_argument(sys.argv[1:])
    parse_card(card_candidate, options)

if __name__ == '__main__':
    sys.exit(main())
