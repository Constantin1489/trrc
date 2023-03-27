echo 'basic_type_front_normal_tab	basic_type_back	basic_type_tag' | ../addstring.py
echo 'basic_type_front_slashtab\tbasic_type_back\tbasic_type_tag' | ../addstring.py
cat test_card_strings.txt | ../addstring.py
../addstring.py 'basic_type_front_stdin	basic_type_back	basic_type_tag'
