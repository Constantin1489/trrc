import sys
import requests
import re
import logging
main_logger = logging.getLogger(__name__)

class bcolors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class ErrorMessages:
    network = f"""
Sending a card to AnkiConnect is failed.
Check list
0. Is your AnkiConnect plugin installed in your Anki?
1. Is your Anki running now? your Anki must be running to use AnkiConnect.
2. Currently AnkiServer is not supported.
3. ip and port config
4. Does your serverside allow port?
    """

def userAnkiConnect(webBindAddress='localhost', webBindPort=8765):

    def webBindAddressHandle(webBindAddress):
        """
        Return string pattern
        if there is http:// or https://, r'{Address}:{Port}'
        else, r'http://{Address}:{Port}'
        """

        if ('http://' or 'https://') in webBindAddress:
            return r"{Address}:{Port}"
        else:
            return r"http://{Address}:{Port}"

    def get_AnkiConnect_URL(webBindAddress, webBindPort):
        urlPattern = webBindAddressHandle(webBindAddress)
        return urlPattern.format(Address=webBindAddress, Port=webBindPort)
        
    return get_AnkiConnect_URL(webBindAddress, webBindPort)

class card:
    """
    A class for card object
    """

    def __init__(self, deck: str, notetype: str, card_str: str, column: list[str], IFS='\t'):
        """
        no deck and notetype. because cardlist has deck and notetype.
        """
        # TODO : argparse IFS
        self.deck: str = deck
        self.notetype: str = notetype

        # TODO : this may cause wrong split error.
        # for example, escape key cards.
        # TODO : argparse IFS
        main_logger.debug(f'investigate {IFS=}: {type(IFS)=}')
        main_logger.debug(f'investigate {card_str=}: {type(card_str)=}')
        self.card_contents_list: list[str] = card_str.split(sep=IFS)
        main_logger.debug(f'investigate {self.notetype=}: {type(self.notetype)=}')
        main_logger.debug(f'investigate {self.card_contents_list=}: {type(self.card_contents_list)=}')
        self.content, self.tag = self.make_card(self.notetype, self.card_contents_list, column)
        main_logger.debug(f'investigate {self.content=}: {type(self.content)=}')
        main_logger.debug(f'investigate {self.tag=}: {type(self.tag)=}')
        #self.content: dict[str, str], self.tag: list[str] = self.make_card(self.deck, self.notetype, self.card_contents_list)
        self.card: tuple[dict[str], list[str]] = self.content, self.tag
        main_logger.debug(f'investigate {self.card=}: {type(self.card)=}')
        #self.card: tuple[dict[str,str], list[str]] = self.content, self.tag

    def __check_notetype(self, notetype, card_contents_list: list[str], column: list[str]):
        """ 
        return card content variables per notetype.
        """

        if column is None and notetype in ['basic', 'Basic', 'BasicTwo']:
            main_logger.debug('basic is on')
            front = card_contents_list[0]

            try:
                back = card_contents_list[1]

            # if card_contents_list[1] doesn't exist, then return None.
            except IndexError:
                main_logger.debug(f'index error: {card_contents_list=}\n{type(card_contents_list)=}')
                return None

            # tag does not need to be splited
            # TODO : def function
            # suggestion : len(list) condition
            tag = self.__is_tag(back, card_contents_list[-1])
            tag = self.__is_Notag(tag)

            # is it good idea? obj: json
            return { 'front' : front, 'back' : back }, tag

        # TODO : import config from outside.
        # TODO : len(cloze) < 3 OR search('\t') OR search('\\t') < 2, check 'tag:' OR make error 
        if column is None and notetype in ['cloze', 'Cloze']:
            main_logger.debug('cloze is on')
            Text = self.__contain_cloze_tag(card_contents_list[0])
            # suggestion : len(list) condition
            try:
                Extra = card_contents_list[1]
            except IndexError:
                Extra = ''

            # TODO: if len(card_contents_list) == 1, __is_tag's parameter is inapropriate.
            # in this case, tag will be Text.
            # in this case, parameter should be Text, card_contents_list[-1] 

            tag = ''
            if Text != card_contents_list[-1]:
            # if a record has only Text, then list[-1] is the Text. This cause
            #an error. 
                tag = self.__is_tag(Extra, card_contents_list[-1])

            tag = self.__is_Notag(tag)

            return { 'Text' : Text, 'Extra' : Extra }, tag

        if column is not None:
            main_logger.debug('column is on')
            merged_contents: dict = self.__merge_card_contents_list_W_column(column, card_contents_list)
            if ('tag' or 'tags') not in column:
                return merged_contents, ['']

            try:
                tag: str = merged_contents.pop('tag')
                tag: list = tag.split(sep=' ')

            except:
                tag: str = merged_contents.pop('tags')
                tag: list = tag.split(sep=' ')

            return merged_contents, tag
        
        print(bcolors.FAIL + bcolors.BOLD + "ERROR: 'def __check_notetype' No predefined notetype is here", bcolors.ENDC, file=sys.stderr)
        print(bcolors.BOLD + "suggestion: use --type and --column option." + bcolors.ENDC, file=sys.stderr)

    def __merge_card_contents_list_W_column(self, column: list, card_contents_list: list):

        if len(column) >= len(card_contents_list):
            return dict(zip(column, card_contents_list))
        raise Exception('column is smaller than actual contents of a card')

    def __is_Notag(self, tag):
        if isinstance(tag, type(None)):
            return ''
        else:
            return tag

    def __is_tag(self, last_item_except_tag, tag_item):
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

        # Last item should not be a tag
        if last_item_except_tag == tag_item:
            return None
        
        if last_item_except_tag != tag_item:
            return tag_item.split(' ')

    def __contain_cloze_tag(self, clozeContent):
        """
        check whether Text contains cloze tag. if not, report and skip.
        """
        # TODO [] : break if failed.
        if re.search(r'{{c\d+::.*}}', clozeContent):
            return clozeContent
        else:
            # TODO : How to skip to next loop
            print(bcolors.FAIL +bcolors.BOLD + f"{clozeContent} does not have any cloze tag", bcolors.ENDC, file=sys.stderr)
            # this break all loops.
            return None

    def make_card(self, notetype, splited_card_list, column):
        """
        return final card object to add DB.
        card: tuple[self.content: dict[str, str], self.tag: list[str]]
        """

        try:
            card: tuple = self.__check_notetype(notetype, splited_card_list, column)
        except Exception as e:
            print('ERROR', e)

        return card

# TODO: put AnkiConnectURL in argument
def create_card(AnkiConnect_URL, card):
    """
    send a json card to a AnkiConnect to create a card.
    card: Type[ankiadderall.card]
    card.deck: str
    card.notetype: str
    card.tag: list[str]
    card.content: dict[str: str]
    """


    # TODO: what the fuck is [ *card.tag ]
    #main_logger.debug(f'investigate {card.notetype=}: {type(card.notetype)=}')
    CARD_JSON: dict = { "action": "addNote",
                       "version": 6,
                       "params": { "note": { "deckName": card.deck,
                                            "modelName": card.notetype,
                                            "fields": card.content,
                                            "tags": card.tag } } }

    main_logger.debug(f'investigate {CARD_JSON=}: {type(CARD_JSON)=}')
    #main_logger.debug(f'{CARD_JSON=}\n{type(CARD_JSON)=}')
    try:
        r = requests.post(AnkiConnect_URL, json=CARD_JSON)
        print(r)

    except:
        # TODO : return the whole line
        main_logger.debug(bcolors.FAIL +bcolors.BOLD + "Sending a card to AnkiConnect is failed" + bcolors.ENDC)
