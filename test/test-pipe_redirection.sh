echo 'basic_type_front	basic_type_back	basic_type_tag' | ../addstring.py
echo 'basic_type_front\tbasic_type_back\tbasic_type_tag' | ../addstring.py
cat test_card_strings.py | ../addstring.py
../addstring.py 'basic_type_front	basic_type_back	basic_type_tag'
