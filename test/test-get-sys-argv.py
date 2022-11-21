import sys
# insert custom module path to the end of the PATH
sys.path.append('/Users/constantinhong/TODO/ankiconnect-script')
import ankiadderall

a = ankiadderall.card(*sys.argv)
print(a.card)
