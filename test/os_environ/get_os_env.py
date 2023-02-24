import os
import sys

# TO get a result : export ANKIADDERAL_DECK='LINUX'
#print(os.environ['ANKIADDERALL_DECK'])


# investigate type
print("{} {} ".format(os.environ['ANKIADDERALL_DECK'], type(os.environ['ANKIADDERALL_DECK'])))
DECK = os.environ['ANKIADDERALL_DECK'] if 'ANKIADDERALL_DECK' in os.environ.keys() else None
TYPE  = os.environ['ANKIADDERALL_DECK'] if 'ANKIADDERALL_DECK' in os.environ.keys() else None
print(DECK)


print(os.environ.keys())
