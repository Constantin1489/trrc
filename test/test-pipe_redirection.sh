echo "test 1"
echo '1basic_type_front_normal_tab with option	basic_type_back	test' | ../ankiadderall/addstring.py -D "Linux::algo"
echo "test 2"
echo '2basic_type_front_normal_tab	basic_type_back	test' | ../ankiadderall/addstring.py
echo "test 2-1"
echo '3basic_type_front_normal_tab_debug	basic_type_back	test' | ../ankiadderall/addstring.py --debug
echo "test 3"
echo '4basic_type_front_slashtab\tbasic_type_back\ttest' | ../ankiadderall/addstring.py
echo "test 4"
cat test_card_strings.txt | ../ankiadderall/addstring.py
#echo "test 4-1"
#cat test_card_strings.txt | ../ankiadderall/addstring.py --debug
echo "test 4-2"
cat test_card_strings-empty.txt | ../ankiadderall/addstring.py --debug
echo "test 4-3"
cat test_card_strings-empty2.txt | ../ankiadderall/addstring.py --debug
echo "test 4-4"
../ankiadderall/addstring.py --debug test_card_strings2.txt
echo "test 4-5: duplicate of the test 4-4"
../ankiadderall/addstring.py -f test_card_strings2.txt
echo "test 5"
../ankiadderall/addstring.py '11basic_type_front_stdin	basic_type_back	test'
echo "test 6"
../ankiadderall/addstring.py -D 'Linux::algo' '12basic_type_front_stdin_withdeck_option	basic_type_back	test'
echo "test 7"
ANKIADDERALL_DECK='somedeck' ANKIADDERALL_TYPE='cloze1' ../ankiadderall/addstring.py '13env_variable_basic_type_front_stdin	basic_type_back	test'
echo "test 8"
../ankiadderall/addstring.py --ip 192.123.123.123 --port 1234 --debug -f test_card_strings2.txt
echo "test 9: cloze with basic"
cat cloze_with_basic_string.txt | ../ankiadderall/addstring.py
#cat cloze_with_basic_string.txt | ../ankiadderall/addstring.py --debug
echo "test 10: cat cloze test"
cat test_cloze.txt | ../ankiadderall/addstring.py
echo "test 11: empty lines"
cat various_empty_lines.txt | ../ankiadderall/addstring.py
echo "test 12: field option"
../ankiadderall/addstring.py --field 'back:front:tag' $'back\t20testfront\ttest' --debug
echo "test 12-1: recognized cloze but improper field. must fail"
../ankiadderall/addstring.py --field 'back:front:tag' $'{{c1::21back}}\t21testfront\ttest' --debug
echo "test 13: deck doesn't exist"
../ankiadderall/addstring.py -D '22asfasdf' 'some<br>	bas	test'
