#!/usr/bin/env python
"""
A command line interface for trrc.
"""

import sys
from .create_parser import parse_argument, parse_card

def main():
    """
    A function for a command line interface.
    """

    card_candidate, options = parse_argument(sys.argv[1:])
    parse_card(card_candidate, options)

if __name__ == '__main__':
    sys.exit(main())
