#!/usr/local/bin/python
import sys
import requests
import re

class bcolors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class userAnkiConnect:
    """
    A class for an AnkiConnect user configure .
    """

#    _webBindAddress = 'localhost'
#    _webBindPort = 8765


    def __init__(self, webBindAddress='localhost', webBindPort=8765):
        """
        A class used to represent an AnkiConnect Configure

        webBindAddress: str 
            a webBindAddress in your AnkiConnect confirue.
        webBindPort: int
            a webBindPort in your AnkiConnect confirue.
        """

        self._webBindAddress = webBindAddress
        self._webBindPort = webBindPort

    def webBindAddressHandle(self, webBindAddress):
        """
        if there is http:// or https://, r'{Address}:{Port}'
        else, r'http://{Address}:{Port}'
        """

        if 'http://' or 'https://' in webBindAddress:
            return r"{Address}:{Port}"
        else:
            return r"http://{Address}:{Port}"

    def get_AnkiConnect_URL(self):
        urlPattern = self.webBindAddressHandle(self._webBindAddress)
        return urlPattern.format(Address=self._webBindAddress, Port=self._webBindPort)
        
class card:
    def __init__(self, deck, notetype, card_str):
        """
        no deck and notetype. because cardlist has deck and notetype.
        """

        # TODO : argparse IFS
        self.deck = deck
        self.notetype = notetype

        # TODO : this may cause wrong split error.
        # for example, escape key cards.
        # TODO : argparse IFS
        self.card_list = card_str.split(sep='\t')
        self.content, self.tag = self.make_card(self.deck, self.notetype, self.card_list)
        self.card = self.content, self.tag

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
            tag = self.is_Notag(tag)

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

            tag = self.is_Notag(tag)

            return { 'Text' : Text, 'Extra' : Extra }, tag

    def is_Notag(self, tag):
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

def create_card(card):
    """
    send a json card to a AnkiConnect to create a card.
    """

    CLOZE_CARD={ "action": "addNote", "version": 6, "params": { "note": { "deckName": card.deck , "modelName":
                                                                         card.notetype, "fields": card.content , "tags":
                                                                         [ *card.tag ] } } }

    # TODO : logging
    print("#####alt version########")
    print(CLOZE_CARD)
    try:
        # TODO : ankiconnectURL
        # TODO : ankiconnectPORT
        r = requests.post('http://127.0.0.1:8765', json=CLOZE_CARD)
        print(r)

    except:
        # TODO : return the whole line
        print(bcolors.FAIL +bcolors.BOLD + "failed" + bcolors.ENDC, file=sys.stderr)
