#!/bin/sh

while read -r line;
do
	#echo $line
	python3 ankiadderall.py "$line"
done < $@
