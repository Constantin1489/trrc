import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall

# test example : $python test-class-card.01.py linux cloze 'front back tag'


# 중복된 카드는 추가가 되지 않는다.
for i in ['../resource/oneway01-example.txt', \
    '/Users/constantinhong/TODO/ankiconnect-script/resource/oneway02-example.txt']:
    with open(i, encoding = 'utf-8') as f:
        for line in f.read().splitlines():
            #print(line)
            #ankiadderall.card('linux', 'Basic', line).make_card()
            a = ankiadderall.card('linux', 'Basic', line)
            print(a.card)

# ERROR :  Ctrl a "        [gnu screen] windowlist menu


