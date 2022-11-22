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
        try:
            self.add_DB()
        except:
            print("failed")


    def check_notetype(self, notetype, card_list):
        ''' return card content variables per notetype'''
        if notetype in ['basic', 'Basic', 'BasicTwo']:
            front = card_list[0]
            back = card_list[1]
            # tag does not need to be splited
            tag = self.is_tag(card_list[1], card_list[-1])
            self.is_None(tag)
            return { 'front' : front, 'back' : back }, tag

        # TODO : import config from outside.
        # TODO : len(cloze) < 3 OR search('\t') < 2, check 'tag:' OR make error 
        if notetype in ['cloze', 'Cloze']:
            Text = self.contain_cloze_tag(card_list[0])
            Extra = card_list[1]
            tag = self.is_tag(card_list[1], card_list[-1])
            self.is_None(tag)
            return { 'Text' : Text, 'Extra' : Extra }, tag

    def is_None(self, tag):
        if isinstance(tag, type(None)):
            sys.exit(1)

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
            # this causes error : test-import-multiple-card.02-cloze.py
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
            return None
    
    def add_DB(self):
        ''' add a card via ankiconnect '''
#
#        # TODO : dict에서 특정한 (key value)만 필터링하기 힘듬. 따라서 전단계에서 나누기
        self.CLOZE_CARD2={ "action": "addNote", "version": 6, "params": { "note": { "deckName": self.deck , "modelName": self.notetype, "fields": self.card , "tags": [ *self.tag ] } } }
        # card, tag = *self.make_card()
        r = requests.post('http://127.0.0.1:8765', json=self.CLOZE_CARD2)
        


    def classify_argv(self, argv):
        ''' check is it string contain a card OR a file.'''
        pass

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
