import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall

# test example : $python test-class-card.01.py linux cloze 'front back tag'


custom_cloze = "some long cloze sentence\t\tTAG"

for i in ['../resource/cloze01-example.txt']:
    with open(i, encoding = 'utf-8') as f:
        for line in *f.read().splitlines(), custom_cloze:
            print(line)
            #ankiadderall.card('linux', 'Basic', line).make_card()
            a = ankiadderall.card('ETC', 'cloze', line)
            print(a.card)



#print("###custom cloze###")
#ankiadderall.card('linux', 'cloze', custom_cloze)

# ERROR :  Ctrl a "        [gnu screen] windowlist menu


