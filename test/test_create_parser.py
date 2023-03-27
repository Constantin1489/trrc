import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from create_parser import create_parser
# create_parser.create_parser

def test_create_parser():
    parser = create_parser()

    result = parser.parse_args('-p 30 some'.split())
    assert  result.port == 30

    result = parser.parse_args()
    assert  result.port == 8765
