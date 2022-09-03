#!/bin/sh
ankiadderall='/Users/constantinhong/TODO/ankiconnect-script/ankiadderall.py'
while read -r line;
do
	#echo $line
	python3 $ankiadderall "$line"
done < $@
