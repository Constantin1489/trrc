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

#TODO DB에서 덱리스트를 조회하는 기능, 카드타입 및 갯수를 조회하는 기능, 타입의 placeholder도 확인하기
#TODO DB에서 input card의 덱이 조회되지 않을 때, 덱리스트 fuzzy하는 기능
#TODO shellscript 실행 후 내부에서 dynamic하게 파일을 선택할 수 있나?
# #라는 문장이 맨 처음에 입력시 스킵하는 기능
#TODO use Object or class for other card type
#TODO change the way make cards
#TODO make specify deck, and notetype from shellscipt

card=arguments2[1].split(sep='\t')
#deckname=arguments2[0].split(sep='\t')
#notetype=arguments2[1].split(sep='\t')
#card=arguments2[2].split(sep='\t')

#arguments 0 ankiadderall.py file name
#arguments 1 deckname
#arguments 2 notetype
#arguments 3 front
#arguments 4 back
#arguments 5 tag


#BASIC notetype
deckname = card[0] #TODO change to #
notetype = card[1] #TODO change to #
front = card[2]
back = card[3]
tag = card[4].split(sep=' ')

#print(deckname, '-', notetype, '-', front, '-', back, '-', tag)

BASIC_CARD={ "action": "addNote", "version": 6, "params": { "note": { "deckName": deckname , "modelName": notetype, "fields": { "Front": front, "Back": back }, "tags": [ *tag ], "audio": { "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ", "filename": "yomichan_ねこ_猫.mp3", "skipHash": "7e2c2f954ef6051373ba916f000168dc", "fields": [ "Front" ] } } } }


r = requests.post('http://127.0.0.1:8765', json=BASIC_CARD)
# 사실 위의 코드만 있어도 충분히 post가 된다. 하지만 아래가 없으면 \
# 에러를 확인할 수 없다.
# {'result': None, 'error': 'model was not found: 4Basic sakdfsdafkasdjv without double qoutes'}
#TODO 이런 에러가 없다면, 카드를 완성된 카드 목록으로 옮기기 EXIT STATUS로 만들기
print(r.json())
