#!/bin/sh
#ankiadderall='/Users/constantinhong/TODO/ankiconnect-script/ankiadderall.py'
ankiadderall='/Users/constantinhong/TODO/ankiconnect-script/ADA_add_one_way.py'
while read -r line;
do
	#echo $line
	python3 $ankiadderall "$line"
done < $@
