import sys
import os
import requests
import re
import logging
main_logger = logging.getLogger(__name__)

class bcolors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Regex_Pattern:
    prevent_HTML_interpret_pattern =  { '<' : '&lt',
                                       '>' : '&gt'}
    newline_to_html_br_pattern = { '\\n' : '<br>',
                                  '\\\\n' : '&#92n' }
    str_to_html_pattern = { ' ' : '&nbsp'}

    def __init__(self):
        self.prevent_HTML_interpret_compile = re.compile("(%s)" % "|".join(map(re.escape, self.prevent_HTML_interpret_pattern.keys())))
        self.newline_to_html_br_compile = re.compile("(%s)" % "|".join(map(re.escape, self.newline_to_html_br_pattern.keys())))
        self.str_to_html_compile = re.compile("(%s)" % "|".join(map(re.escape, self.str_to_html_pattern.keys())))

class ErrorMessages:
    ask_check_network = f"""
Sending a card to AnkiConnect is failed.
Check list
1. Is your Anki running now? your Anki must be running to use AnkiConnect.
2. Is your AnkiConnect plugin installed in your Anki application and enabled?
3. Is an ip and port config correct?
4. Does your serverside allow port?
"""
    connect_time_out = "It's a connection time out."
    unknown_network_error = """It's an unknown error.
Please report it to https://github.com/Constantin1489/ankistreamadd/issues"""
    basictype = 'Basic type must have at least two fields'
    wrong_field = '"cannot create note because it is empty"'
    check_notetype = "ERROR: 'def _check_notetype' No predefined notetype is here"
    type_field_suggestion = "suggestion: use --type and --field option."
    read_timed_out = """It's a Read timed out. But it is possible your Anki server is handling
cards now. Within a minute, Your card is maybe available. If you set
to do sync, this program will ignore it by now. Please, sync manually
with '--sync' option without card contents in a command line after a while"""
    valid_api_key_require = "valid api key must be provided. please check your apikey and, use --apikey option or add it into a config file."

def ErrorMessageColoring(ErrorMessageString, message_type=None):
    if message_type == 'ERROR':
        errormessage =  f'ERROR message: {ErrorMessageString}'
    else:
        errormessage =  f'{bcolors.FAIL + bcolors.BOLD + ErrorMessageString + bcolors.ENDC}'
    print(errormessage, file=sys.stderr)

def userAnkiConnect(webBindAddress='localhost', webBindPort=8765):

    def webBindAddressHandle(webBindAddress):
        """
        Return string pattern
        if there is http:// or https://, r'{Address}:{Port}'
        else, r'http://{Address}:{Port}'
        """

        if webBindAddress[:5] in {'http:', 'https'}:
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

    def __init__(self, deck: str, notetype: str, card_str: str, field: str,
                 cloze_field, cloze_type, IFS='\t'):
        """
        no deck and notetype. because cardlist has deck and notetype.
        """

        self.deck: str = deck
        self.notetype: str = notetype
        self.card_str = card_str
        self.field: str = field
        self.IFS = IFS
        self.cloze_field = cloze_field
        self.cloze_type = cloze_type

        main_logger.debug(f'card object: {self.notetype=}: {type(self.notetype)=}')
        main_logger.debug(f'card object: {IFS=}: {type(IFS)=}')
        main_logger.debug(f'card object: {card_str=}: {type(card_str)=}')

    # TODO: cloze fallback
    def _check_notetype(self, notetype, splited_card_list: list[str], field: list[str]):
        """
        return card content variables per notetype.
        """

        if field is None and notetype in ['basic', 'Basic']:
            main_logger.debug('hard coded basic is on')
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
        if field is None and notetype in ['cloze', 'Cloze']:
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

            return { 'Text' : Text, 'Back Extra' : Extra }, tag

        if field:
            main_logger.debug('field is on')
            if notetype in ['cloze', 'Cloze']:
                if self.cloze_field:
                    merged_contents: dict = self._merge_splited_card_list_W_field(self.get_field(self.cloze_field), splited_card_list)
                else:
                    merged_contents: dict = self._merge_splited_card_list_W_field(field, splited_card_list)

            else:
                merged_contents: dict = self._merge_splited_card_list_W_field(field, splited_card_list)

            if ('tag' or 'tags') not in field:
                return merged_contents, ['']

            try:
                tag: str = merged_contents.pop('tag')

            except:
                tag: str = merged_contents.pop('tags')

            tag: list = tag.split(sep=' ')

            return merged_contents, tag

        print(bcolors.FAIL + bcolors.BOLD + ErrorMessages.check_notetype, bcolors.ENDC, file=sys.stderr)
        print(bcolors.BOLD + ErrorMessages.type_field_suggestion + bcolors.ENDC, file=sys.stderr)

    def _merge_splited_card_list_W_field(self, field: list, card_contents_list: list):

        if len(field) >= len(card_contents_list):
            return dict(zip(field, card_contents_list))
        raise Exception('a number of the fields in the option is smaller than actual fields of a card content')

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

    def prevent_HTML_interpret(self, regex_compile, pattern):

        # For each match, look-up corresponding value in dictionary
        self.card_str = regex_compile.sub(lambda mo: pattern[mo.group()], self.card_str)

    def newline_to_html_br(self, regex_compile, pattern):

        self.card_str = regex_compile.sub(lambda mo: pattern[mo.group()], self.card_str)

    def import_if_file(self, regex_compile, pattern):

        def str_to_html(asrting, regex_compile, pattern):

            return  regex_compile.sub(lambda mo: pattern[mo.group()], self.card_str)

        card_contents = []
        for f in self.card_str.split(sep=self.IFS):
            if os.path.isfile(f):
                lines_of_the_file = []
                with open(f) as f:
                    lines_of_the_file += f.read().splitlines()
                card_contents.append(str_to_html('\\n'.join(lines_of_the_file)))

            else:
                card_contents.append(f)

        self.card_str = self.IFS.join(card_contents)
        main_logger.debug(f'import_if_a_file {self.card_str}')

    def make_card(self):
        """
        return final card object to add DB.
        card: tuple[self.content: dict[str, str], self.tag: list[str]]
        """

        try:
            self.content, self.tag = self._check_notetype(self.notetype,
                                                          self.card_str.split(sep=self.IFS),
                                                          self.get_field(self.field))

        except Exception as e:
            print('ERROR', e, file=sys.stderr)

    def get_field(self, field):
        if field is None:
            return None
        return (lambda s: [i for i in s.split(':')])(field)

    def create_cardjson_note(self):
        """
        create a card note to insert into a Note list to use 'addNotes'

        card.deck: str
        card.notetype: str
        card.tag: list[str]
        card.content: dict[str: str]
        """

        return { "deckName": self.deck,
                "modelName": self.notetype,
                "fields": self.content,
                "tags": self.tag }
