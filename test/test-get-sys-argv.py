import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall

string = sys.argv
print(sys.argv)
print(sys.argv[1:])
a = ankiadderall.card(*sys.argv[1:])
print(a.card, a.tag)
# bug
print(a.CLOZE_CARD2)
