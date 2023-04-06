echo "test 1"
echo '1basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | ../addstring.py -D "Linux::algo"
echo "test 2"
echo '2basic_type_front_normal_tab	basic_type_back	basic_type_tag basic_type_tag2' | ../addstring.py
echo "test 2-1"
echo '3basic_type_front_normal_tab_debug	basic_type_back	basic_type_tag' | ../addstring.py --debug
echo "test 3"
echo '4basic_type_front_slashtab\tbasic_type_back\tbasic_type_tag' | ../addstring.py
echo "test 4"
cat test_card_strings.txt | ../addstring.py
#echo "test 4-1"
#cat test_card_strings.txt | ../addstring.py --debug
echo "test 4-2"
cat test_card_strings-empty.txt | ../addstring.py --debug
echo "test 4-3"
cat test_card_strings-empty2.txt | ../addstring.py --debug
echo "test 4-4"
../addstring.py --debug test_card_strings2.txt
echo "test 4-5"
../addstring.py -f test_card_strings2.txt
echo "test 5"
../addstring.py '11basic_type_front_stdin	basic_type_back	basic_type_tag'
echo "test 6"
../addstring.py -D 'Linux::algo' '12basic_type_front_stdin_withdeck_option	basic_type_back	basic_type_tag'
echo "test 7"
ANKIADDERALL_DECK='somedeck' ANKIADDERALL_TYPE='cloze1' ../addstring.py '13env_variable_basic_type_front_stdin	basic_type_back	basic_type_tag'
echo "test 8"
../addstring.py --ip 192.123.123.123 --port 1234 --debug -f test_card_strings2.txt
echo "test 9: cloze with basic"
cat cloze_with_basic_string.txt | ../addstring.py
#cat cloze_with_basic_string.txt | ../addstring.py --debug
echo "test 10: cat cloze test"
cat test_cloze.txt | ../addstring.py
echo "test 11: empty lines"
cat various_empty_lines.txt | ../addstring.py
