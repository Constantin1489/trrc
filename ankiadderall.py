#!/usr/local/bin/python
import sys
import requests

class card:
    def __init__(self, deck, notetype, card_list):
        ''' no deck and notetype. because cardlist has deck and notetype. '''
        deck = deck
        notetype = notetype
        # TODO : this may cause wrong split error.
        # for example, escape key cards.
        card_list = card_list.split(sep='\t')
        #card  = self.check_notetype(notetype, card_list)
        print(self.make_card(deck, notetype, card_list))
        #print(self.make_card(deck, notetype, **card))
        #print("deck: {}\nnotetype: {}\nfront: {}\nback: {}\ntag: {}\n".format(deck, notetype, *card))

    def check_notetype(self, notetype, card_list):
        ''' return card content variables per notetype'''
        if notetype in ['Basic', 'BasicTwo']:
            front = card_list[0]
            back = card_list[1]
            # tag does not need to be splited
            #tag = card_list[3].split(sep=' ')
            tag = self.is_tag(card_list[1], card_list[-1])
            #print("card[1] {} card[-1] {} ".format(card_list[1], card_list[-1]))
            #tag = card_list[2]
            return { 'front' : front, 'back' : back, 'tag': tag }

        # TODO : import config from outside.
        if notetype in ['cloze', 'Cloze']:
            pass

    def make_card(self, deck, notetype, card_list):
        card = self.check_notetype(notetype, card_list)
        return { 'deck' : deck,\
                'notetype' : notetype,\
                **card }
        
    def is_tag(self, last_item_except_tag, tag_item):
        '''
        last card item can not be tag item.
        therefore, if they are the same, there is no tag.
        '''
        if last_item_except_tag == tag_item:
            return None
        

        if last_item_except_tag != tag_item:
            return tag_item


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
