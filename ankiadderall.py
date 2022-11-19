#!/usr/local/bin/python
import sys
import requests

class card:
    def __init__(self, deck, notetype, card_list):
        ''' no deck and notetype. because cardlist has deck and notetype. '''
        deck = deck
        notetype = notetype
        card_list = card_list.split(sep='\t')
        #card_list = card_list.split(sep=' ')
        card  = self.check_notetype(notetype, card_list)
        print("deck: {}\nnotetype: {}\nfront: {}\nback: {}\ntag: {}\n".format(deck, notetype, *card))

    def check_notetype(self, notetype, card_list):
        if notetype in ['Basic', 'BasicTwo']:
            front = card_list[0]
            back = card_list[1]
            # tag does not need to be splited
            #tag = card_list[3].split(sep=' ')
            tag = card_list[2]
            return front, back, tag
        

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
