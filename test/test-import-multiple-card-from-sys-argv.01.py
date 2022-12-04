import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall

# test example : $python test-class-card.01.py linux cloze 'front back tag'


# TODO [] :중복된 카드는 추가가 되지 않는다.
# TODO [] :실패한 카드는 stderr로 표시한다.

#for line in f.read().splitlines():

line = sys.argv[1:]
#print(line)
print("{}{}".format(line, type(line)))
print(line)
a = ankiadderall.card('linux', 'Basic', *line)
print(a.card)

# ERROR :  Ctrl a "        [gnu screen] windowlist menu


