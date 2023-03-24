#!/usr/local/bin/python

import sys
import re
import os
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiadderall')
import ankiadderall
import argparse

def makeParser():
    pass

def parse_argument(argv):
    # if there is a file or a string input, use it as input
    if len(sys.argv) > 1:
        card_candidate = sys.argv[1:]
        return card_candidate

    else:

        # if there is pipe redirection, use it as input
        if not sys.stdin.isatty(): 

            # remove trailing \n in its card candidate.
            card_candidate = [card.rstrip('\n') for card in sys.stdin.readlines()]
            return card_candidate

        # show an usage if no input nor file nor pipe redirection.
        else:
            # TODO : argparse
            print("""usage: addstring [file ...]
            cat [file ...] | addstring""")
            exit(2)


def parse_card(card_candidate):
    for i in card_candidate:

        if os.path.isfile(i):

            # print file name
            print(i, file=sys.stdout)

            with open(i) as f:
                lines = f.read().splitlines()

            for j in lines:

                # skip empty line.
                if not j:
                    continue

                # if a line has cloze tag, than the line is a cloze type.
                if re.findall(r'{{c\d::.*}}', j):
                    a = ankiadderall.card(DECK, 'cloze', j)

                else:
                    a = ankiadderall.card(DECK, TYPE, j)

                print(a.card, file=sys.stdout)

        # if i is not a file, then consider i as a string and make a card.
        else:
            # print statements are for debug
            #print("{} type {}".format(i, type(i)))
            #print("{} type {}".format(i.encode("unicode_escape"), type(i)))
            #print("{} ".format(i.isascii()))
            #print(isinstance(i, bytes))
            #i = unicode(i, "utf-8")
            a = ankiadderall.card(DECK, TYPE, i)
            print(a.card)

if __name__ == '__main__' :

    ANKIADDERALL_CONFIG = { 'DECK': 'Linux', 'TYPE':'Basic'  }

    # assign a card deck.
    # seek the shell env variable. if it doesn't exist, then use a compiled DECK value.
    # let's just get all environment value and check all.
    # if deck and type is not configed then use Anki program default Deck and card type setting.
    DECK = os.environ['ANKIADDERALL_DECK'] if 'ANKIADDERALL_DECK' in os.environ.keys() else ANKIADDERALL_CONFIG['DECK']
    TYPE  = os.environ['ANKIADDERALL_TYPE'] if 'ANKIADDERALL_TYPE' in os.environ.keys() else ANKIADDERALL_CONFIG['TYPE']

    card_candidate = parse_argument(sys.argv)
    parse_card(card_candidate)
    exit(0)
