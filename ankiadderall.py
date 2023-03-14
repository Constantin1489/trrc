#!/usr/local/bin/python
import sys
import requests
import re

class bcolors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class card:
    def __init__(self, deck, notetype, card_str):
        """
        no deck and notetype. because cardlist has deck and notetype.
        """

        self.deck = deck
        self.notetype = notetype

        # TODO : this may cause wrong split error.
        # for example, escape key cards.
        self.card_list = card_str.split(sep='\t')
        self.content, self.tag = self.make_card(self.deck, self.notetype, self.card_list)
        self.card = self.content, self.tag

        try:
            # TODO[] : put if self.card != None: 
            self.add_DB()
        except:
            # TODO : return the whole line
            print(bcolors.FAIL +bcolors.BOLD + "failed" + bcolors.ENDC, file=sys.stderr)


    def check_notetype(self, notetype, card_list):
        """ 
        return card content variables per notetype.
        """

        if notetype in ['basic', 'Basic', 'BasicTwo']:
            front = card_list[0]

            try:
                back = card_list[1]

            # if card_list[1] doesn't exist, then return None.
            except IndexError:
                # TODO : add stderr
                print("index error", file=sys.stderr)
                return None

            # tag does not need to be splited
            # suggestion : len(list) condition
            tag = self.is_tag(back, card_list[-1])
            tag = self.is_None(tag)

            return { 'front' : front, 'back' : back }, tag

        # TODO : import config from outside.
        # TODO : len(cloze) < 3 OR search('\t') OR search('\\t') < 2, check 'tag:' OR make error 
        if notetype in ['cloze', 'Cloze']:
            Text = self.contain_cloze_tag(card_list[0])
            # suggestion : len(list) condition
            try:
                Extra = card_list[1]
            except IndexError:
                Extra = ''

            # TODO: if len(card_list) == 1, is_tag's parameter is inapropriate.
            # in this case, tag will be Text.
            # in this case, parameter should be Text, Card_list[-1] 

            tag = ''
            if Text != card_list[-1]:
            # if a record has only Text, then list[-1] is the Text. This cause
            #an error. 
                tag = self.is_tag(Extra, card_list[-1])

            tag = self.is_None(tag)

            return { 'Text' : Text, 'Extra' : Extra }, tag

    def is_None(self, tag):
        if isinstance(tag, type(None)):
            return ''
        else:
            return tag

    def make_card(self, deck, notetype, splited_card_list):
        """
        return final card object to add DB.
        """
        card = self.check_notetype(notetype, splited_card_list)
        return card


    def is_tag(self, last_item_except_tag, tag_item):
        """
        last card item can not be tag item.
        therefore, if they are the same, there is no tag.
        """
        if tag_item == '':
            """
            this prevent to compare empty tag and last item of cloze
            therefore, cloze can have only one item.
            """
            return ''

        if last_item_except_tag == tag_item:
            return None
        
        if last_item_except_tag != tag_item:
            return tag_item.split(' ')


    def contain_cloze_tag(self, cloze):
        """
        check whether Text contains cloze tag. if not, report and skip.
        """
        # TODO [] : break if failed.
        if re.search(r'{{c\d+::.*}}', cloze):
            return cloze
        else:
            # TODO : How to skip to next loop
            # TODO : return stderr
            print("does not have any cloze tag", file=sys.stderr)
            # this break all loops.
            return None

    def add_DB(self):
        """
        add a card via ankiconnect
        """

#        # TODO : dict에서 특정한 (key value)만 필터링하기 힘듬. 따라서 전단계에서 나누기

        self.CLOZE_CARD2={ "action": "addNote", "version": 6, "params": { "note": { "deckName": self.deck , "modelName": self.notetype, "fields": self.content , "tags": [ *self.tag ] } } }
        print(self.CLOZE_CARD2)
        r = requests.post('http://127.0.0.1:8765', json=self.CLOZE_CARD2)
        print(r)

    def classify_argv(self, argv):
        """
        check is it string contain a card OR a file.
         if len(card_list) == 1:; is_file(card_list[0])
         """
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
