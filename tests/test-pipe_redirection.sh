echo "test 1"
echo '1basic_type_front_normal_tab with option	basic_type_back	test' | trrc -D "Linux::algo"
echo "test 2"
echo '2basic_type_front_normal_tab	basic_type_back	test' | trrc
echo "test 2-1"
echo '3basic_type_front_normal_tab_debug	basic_type_back	test' | trrc --debug
echo "test 3"
echo '4basic_type_front_slashtab\tbasic_type_back\ttest' | trrc
echo "test 4"
cat test_card_strings.txt | trrc
#echo "test 4-1"
#cat test_card_strings.txt | trrc --debug
echo "test 4-2"
cat test_card_strings-empty.txt | trrc --debug
echo "test 4-3"
cat test_card_strings-empty2.txt | trrc --debug
echo "test 4-4"
trrc --debug test_card_strings2.txt
echo "test 4-5: duplicate of the test 4-4"
trrc -f test_card_strings2.txt
echo "test 5"
trrc '11basic_type_front_stdin	basic_type_back	test'
echo "test 6"
trrc -D 'Linux::algo' '12basic_type_front_stdin_withdeck_option	basic_type_back	test'
echo "test 7"
ANKIADDERALL_DECK='somedeck' ANKIADDERALL_TYPE='cloze1' trrc '13env_variable_basic_type_front_stdin	basic_type_back	test'
echo "test 8"
trrc --ip 192.123.123.123 --port 1234 --debug -f test_card_strings2.txt
echo "test 9: cloze with basic"
cat cloze_with_basic_string.txt | trrc
#cat cloze_with_basic_string.txt | trrc --debug
echo "test 10: cat cloze test"
cat test_cloze.txt | trrc
echo "test 11: empty lines"
cat various_empty_lines.txt | trrc
echo "test 12: field option"
trrc --field 'back:front:tag' $'back\t20testfront\ttest' --debug
echo "test 12-1: recognized cloze but improper field. must fail. But In new algorithm, this will be a cloze."
trrc --field 'back:front:tag' $'{{c1::21back}}\t21testfront\ttest' --debug
echo "test 13: deck doesn't exist"
trrc -D '22asfasdf' 'some<br>	bas	test'