import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall

# test example : $python test-class-card.01.py linux cloze 'front back tag'
ankiadderall.card(*sys.argv[1:])


