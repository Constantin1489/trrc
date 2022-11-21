#!/usr/local/bin/python
import sys
import requests
import re

class card:
    def __init__(self, deck, notetype, card_str):
        ''' no deck and notetype. because cardlist has deck and notetype. '''
        self.deck = deck
        self.notetype = notetype
        # TODO : this may cause wrong split error.
        # for example, escape key cards.
        self.card_list = card_str.split(sep='\t')
        self.card, self.tag = self.make_card(self.deck, self.notetype, self.card_list)
        self.add_DB()

    def check_notetype(self, notetype, card_list):
        ''' return card content variables per notetype'''
        if notetype in ['basic', 'Basic', 'BasicTwo']:
            front = card_list[0]
            back = card_list[1]
            # tag does not need to be splited
            tag = self.is_tag(card_list[1], card_list[-1])
            return { 'front' : front, 'back' : back }, tag

        # TODO : import config from outside.
        # TODO : len(cloze) < 3 OR search('\t') < 2, check 'tag:' OR make error 
        if notetype in ['cloze', 'Cloze']:
            Text = self.contain_cloze_tag(card_list[0])
            Extra = card_list[1]
            tag = self.is_tag(card_list[1], card_list[-1])
            return { 'Text' : Text, 'Extra' : Extra }, tag

    def make_card(self, deck, notetype, splited_card_list):
        ''' return final card object to add DB. '''
        card = self.check_notetype(notetype, splited_card_list)
        return card
        
    def is_tag(self, last_item_except_tag, tag_item):
        '''
        last card item can not be tag item.
        therefore, if they are the same, there is no tag.
        '''
        if last_item_except_tag == tag_item:
            return None
        
        if last_item_except_tag != tag_item:
            return tag_item.split(' ')


    def contain_cloze_tag(self, cloze):
        ''' check whether Text contains cloze tag. if not, report and skip. '''
        # TODO [] : break if failed.
        if re.search(r'{{c\d+::.*}}', cloze):
            return cloze
        else:
            # TODO : How to skip to next loop
            # TODO : return stderr
            print("does not have any cloze tag")
            exit
    
    def add_DB(self):
        ''' add a card via ankiconnect '''
#        BASIC_CARD={ "action": "addNote", "version": 6, "params": { "note": { "deckName": deckname , "modelName": notetype, "fields": { "Front": front, "Back": back }, "tags": [ *tag ] } } }
#        CLOZE_CARD={ "action": "addNote", "version": 6, "params": { "note": { "deckName": deckname , "modelName": notetype, "fields": { "Front": front, "Back": back }, "tags": [ *tag ] } } }
#
#        # TODO : dict에서 특정한 (key value)만 필터링하기 힘듬. 따라서 전단계에서 나누기
        self.CLOZE_CARD2={ "action": "addNote", "version": 6, "params": { "note": { "deckName": self.deck , "modelName": self.notetype, "fields": self.card , "tags": [ *self.tag ] } } }
        # card, tag = *self.make_card()
        r = requests.post('http://127.0.0.1:8765', json=self.CLOZE_CARD2)
        


# TODO: merge the class below to the class above.
class ankiCardList:
    def __init__(self):
        CardList = None
# []TODO : separate sys.argv from class.
#        arguments2=sys.argv
#        card=arguments2[1].split(sep='\t')
        deckname = None
        notetype = None
        cards = []

    def classify_argv(self, argv):
        ''' check is it string contain a card OR a file.'''
        pass

    def insert_list(self, deck, notetype, file):
        CardList = file
# []TODO : separate sys.argv from class.
#        arguments2=sys.argv
#        card=arguments2[1].split(sep='\t')
        deckname = deck
        notetype = notetype
        cards = []

    def add_from_string(self, string):
# []TODO : make card with a string from sys.argv
# a feature that helps you add card from the selected \
# string using automator, etc.
        pass

    def add_from_file(self, file):
# []TODO : make card with a file path from sys.argv
# a feature that helps you add card from the selected \
# file using automator, cli..
        pass
        return file

    def make_one_card(self, csv_string):
        front = none
        back = none
        tag = none
        card = { front : front, back : back, tag : tag }
        return card

    def is_exist(self):
        ''' check cards in the list already exist in the Anki DB '''
        pass

    def is_error(self):
        ''' check cards whether is there any missing values to key. '''
        pass

    def add_to_Anki(self):
        ''' add all the cards to Anki DB '''
        pass
        ''' use pickle to debug by compare pickles. '''
        #r = requests.post('http://127.0.0.1:8765', json=BASIC_CARD)



#print(card(*sys.argv[1:]))
