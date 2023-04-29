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
1. Is your Anki running now? your Anki must be running to use AnkiConnect.
2. Is your AnkiConnect plugin installed in your Anki application and enabled?
3. Is an ip and port config correct?
4. Does your serverside allow port?
"""
    basictype = 'Basic type must have at least two fields'
    wrong_field = '"cannot create note because it is empty"'
    check_notetype = "ERROR: 'def _check_notetype' No predefined notetype is here"
    type_column_suggestion = "suggestion: use --type and --column option."

def userAnkiConnect(webBindAddress='localhost', webBindPort=8765):

    def webBindAddressHandle(webBindAddress):
        """
        Return string pattern
        if there is http:// or https://, r'{Address}:{Port}'
        else, r'http://{Address}:{Port}'
        """

        if ('http:' or 'https') in webBindAddress[:5]:
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

        self.deck: str = deck
        self.notetype: str = notetype

        main_logger.debug(f'card object: {self.notetype=}: {type(self.notetype)=}')
        main_logger.debug(f'card object: {IFS=}: {type(IFS)=}')
        main_logger.debug(f'card object: {card_str=}: {type(card_str)=}')
        self.json = self.create_cardjson()

    def _check_notetype(self, notetype, splited_card_list: list[str], column: list[str]):
        """
        return card content variables per notetype.
        """

        if column is None and notetype in ['basic', 'Basic', 'BasicTwo']:
            main_logger.debug('basic is on')
            front = splited_card_list[0]

            try:
                back = splited_card_list[1]

            # if splited_card_list[1] doesn't exist, then return None.
            except IndexError:
                main_logger.debug(f'index error: {splited_card_list=}: {type(splited_card_list)=}')
                raise Exception(ErrorMessages.basictype)

            # tag does not need to be splited
            # TODO : def function
            # suggestion : len(list) condition
            tag = self._is_tag(back, splited_card_list[-1])
            tag = self._is_Notag(tag)

            # is it good idea? obj: json
            return { 'front' : front, 'back' : back }, tag

        # TODO : import config from outside.
        # TODO : len(cloze) < 3 OR search('\t') OR search('\\t') < 2, check 'tag:' OR make error
        if column is None and notetype in ['cloze', 'Cloze']:
            main_logger.debug('cloze is on')
            Text = self._cloze_contain_cloze_tag(splited_card_list[0])
            # suggestion : len(list) condition
            try:
                Extra = splited_card_list[1]
            except IndexError:
                Extra = ''

            # TODO: if len(splited_card_list) == 1, _is_tag's parameter is inapropriate.
            # in this case, tag will be Text.
            # in this case, parameter should be Text, splited_card_list[-1]

            tag = ''
            if Text != splited_card_list[-1]:
            # if a record has only Text, then list[-1] is the Text. This cause
            #an error.
                tag = self._is_tag(Extra, splited_card_list[-1])

            tag = self._is_Notag(tag)

            return { 'Text' : Text, 'Extra' : Extra }, tag

        if column is not None:
            main_logger.debug('column is on')
            merged_contents: dict = self._merge_splited_card_list_W_column(column, splited_card_list)
            if ('tag' or 'tags') not in column:
                return merged_contents, ['']

            try:
                tag: str = merged_contents.pop('tag')

            except:
                tag: str = merged_contents.pop('tags')

            tag: list = tag.split(sep=' ')

            return merged_contents, tag

        print(bcolors.FAIL + bcolors.BOLD + ErrorMessages.check_notetype, bcolors.ENDC, file=sys.stderr)
        print(bcolors.BOLD + ErrorMessages.type_column_suggestion + bcolors.ENDC, file=sys.stderr)

    def _merge_splited_card_list_W_column(self, column: list, card_contents_list: list):

        if len(column) >= len(card_contents_list):
            return dict(zip(column, card_contents_list))
        raise Exception('a number of the columns in the option is smaller than actual fields of a card contents')

    def _is_Notag(self, tag):
        if isinstance(tag, type(None)):
            return ''
        else:
            return tag

    def _is_tag(self, last_item_except_tag, tag_item):
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

    def _cloze_contain_cloze_tag(self, clozeContent):
        """
        check whether Text contains cloze tag. if not, report and skip.
        """

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
            card: tuple = self._check_notetype(notetype, splited_card_list, column)

        except Exception as e:
            print('ERROR', e, file=sys.stderr)

    def create_cardjson(self):
        """
        send a json card to a AnkiConnect to create a card.
        card: Type[ankiadderall.card]
        card.deck: str
        card.notetype: str
        card.tag: list[str]
        card.content: dict[str: str]
        """

        return { "action": "addNote",
               "version": 6,
               "params": { "note": { "deckName": self.deck,
                                    "modelName": self.notetype,
                                    "fields": self.content,
                                    "tags": self.tag } } }
