import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall
import os

# test example : $python test-class-card.01.py linux cloze 'front back tag'


# TODO [] :중복된 카드는 추가가 되지 않는다.
# TODO [] :실패한 카드는 stderr로 표시한다.

ANKIADDERALL_CONFIG = { 'DECK': 'Linux', 'TYPE':'Basic'  }



line = sys.argv[1:]

if len(line) == 0:
    print("No card {}".format(line))
    exit(1)

# if it's a file, then read file and run loop to add strings as cards.
if os.path.isfile(*line):
    with 


print("{}{}".format(line, type(line)))


# assign a card deck.
# seek the shell env variable. if it doesn't exist, then use a compiled DECK value.
try:
    DECK = os.environ['ANKIADDERALL_DECK']
except KeyError:
    DECK = ANKIADDERALL_CONFIG['DECK']
    #DECK = 'Linux'

# assign a card type.
try:
    TYPE = os.environ['ANKIADDERALL_TYPE']
except KeyError:
    TYPE = ANKIADDERALL_CONFIG['TYPE']
    #TYPE = 'Basic'


# os.environ['ANKIADDERALL_IFS'] 를 만들어서 스페이스4가 아니면, \t으로 처리할지 정하자.
# 아니면 그냥 \\t같은 것을 이용해서 구분시킬까?

# 이 방식이 옳은가? 이 ankiadderall 안에 따로 datatype를 만들어서, 전부 저장했다가 한꺼번에 처리할 수 있게끔하는게 좋지 않을까?
# python내의 for loop로 저장시켜서.. 아니면 그냥 파일을 input으로 넣어서..
a = ankiadderall.card(DECK, TYPE, *line)
print(a.card)

# ERROR :  Ctrl a "        [gnu screen] windowlist menu
