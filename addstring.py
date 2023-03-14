#!/usr/local/bin/python

import sys
import re
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiadderall')
import ankiadderall
import os

# test example : $python test-class-card.01.py linux cloze 'front back tag'


# TODO [x] :중복된 카드는 추가가 되지 않는다.
# TODO [x] :실패한 카드는 stderr로 표시한다.

ANKIADDERALL_CONFIG = { 'DECK': 'Linux', 'TYPE':'Basic'  }

# assign a card deck.
# seek the shell env variable. if it doesn't exist, then use a compiled DECK value.
# let's just get all environment value and check all.

# if deck and type is not configed then use Anki program default Deck and card type setting.
DECK = os.environ['ANKIADDERALL_DECK'] if 'ANKIADDERALL_DECK' in os.environ.keys() else ANKIADDERALL_CONFIG['DECK']
TYPE  = os.environ['ANKIADDERALL_TYPE'] if 'ANKIADDERALL_TYPE' in os.environ.keys() else ANKIADDERALL_CONFIG['TYPE']


# if there is a file or a string input, use it as input
if len(sys.argv) > 1:
    card_candidate = sys.argv[1:]

else:

    # if there is pipe redirection, use it as input
    if not sys.stdin.isatty(): 

        # remove trailing \n in its card candidate.
        card_candidate = [card.rstrip('\n') for card in sys.stdin.readlines()]

    # show an usage if no input nor file nor pipe redirection.
    else:
        print("""usage: addstring [file ...]
        cat [file ...] | addstring""")
        exit(2)



for i in card_candidate:

    if os.path.isfile(i):

        # print file name
        print(i, file=sys.stdout)

        with open(i) as f:
        #with open(i, encoding='unicode_escape') as f:
            # lines is list of card in a file.
            lines = f.read().splitlines()
            # j is a single card.
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

exit(0)
