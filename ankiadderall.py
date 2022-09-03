import sys
import requests

#internal field separater = \t
#arguments=sys.argv
#arguments=sys.orig_argv
arguments2=sys.argv
#print(arguments)
#print(arguments2)
#print(arguments2[1])
#print(type(arguments2[1]))
#print(arguments2[1].split(sep='\t'))
#print(type(arguments2[1].split(sep='\t')))

#use Object or class
card=arguments2[1].split(sep='\t')

#arguments 0 ankiadderall.py file name
#arguments 1 deckname
#arguments 2 notetype
#arguments 3 front
#arguments 4 back
#arguments 5 tag


#BASIC notetype
deckname = card[0]
notetype = card[1]
front = card[2]
back = card[3]
tag = card[4].split(sep=' ')

print(deckname, '-', notetype, '-', front, '-', back, '-', tag)

BASIC_CARD={ "action": "addNote", "version": 6, "params": { "note": { "deckName": deckname , "modelName": notetype, "fields": { "Front": front, "Back": back }, "tags": [ *tag ], "audio": { "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ", "filename": "yomichan_ねこ_猫.mp3", "skipHash": "7e2c2f954ef6051373ba916f000168dc", "fields": [ "Front" ] } } } }


r = requests.post('http://127.0.0.1:8765', json=BASIC_CARD)
print(r.json())
