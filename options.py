import sys
import os
import re
sys.path.append('/Users/constantinhong/TODO/ankiadderall')
import ankiadderall
# TODO
import argparse

def parse_argument(argv):
    # if there is a file or a string input, use it as input
    if len(argv) > 1:
        card_candidate = argv[1:]
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


def parse_card(card_candidate, DECK, TYPE):
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
                    TYPE = 'cloze'

                a = ankiadderall.card(DECK, TYPE, j)
                # logging
                #print(ankiadderall.userAnkiConnect().get_AnkiConnect_URL())
                ankiadderall.create_card(ankiadderall.userAnkiConnect().get_AnkiConnect_URL(), a)
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
            # logging
            #print(ankiadderall.userAnkiConnect().get_AnkiConnect_URL())
            ankiadderall.create_card(ankiadderall.userAnkiConnect().get_AnkiConnect_URL(), a)
            print(a.card)
