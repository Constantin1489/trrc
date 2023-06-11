import sys
import os
import re
import logging
main_logger = logging.getLogger(__name__)

class ColorsPrint:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class RegexPattern:

   # prevent to read it as a HTML tag
    prevent_html_interpret_pattern =  { '<' : '&lt;',
                                       '>' : '&gt;'
                                       }

    # commandline 'first_sentence\nSecond_sentent'
    # commandline 'This is \\n. It is not new line.'
    newline_to_html_br_pattern = { '\\n' : '<br>',
                                  # new line.
                                  '\\\\n' : '&#92n;'
                                  # escaped new line
                                  }

    # it's for import_if_file_in_content method.
    # read a file as a string for HTML.
    # '@@@': import_if_file_in_content method joins lines of the file with
    # '@@@'(new line). Therefore, to HTML interpret it as a new line, '<br>'
    # '\\\\': '\n' in file is '\\n'. So, to prevent it to be interpret, '&#92;'
    text_file_newline_to_html_br_pattern = { '@@@' : '<br>',
                                            '\\\\' : '&#92;'}

    str_to_html_pattern = { ' ' : '&nbsp;',
                           # it is a space character.
                           '	' : '&emsp;'
                           # it is a tab character.
                           }

    str_to_html_pattern.update(text_file_newline_to_html_br_pattern)
    str_to_html_pattern.update(prevent_html_interpret_pattern)

    def __init__(self):
        self.prevent_html_interpret_compile = re.compile("|".join(map(re.escape, self.prevent_html_interpret_pattern.keys())))
        self.newline_to_html_br_compile = re.compile("|".join(map(re.escape, self.newline_to_html_br_pattern.keys())))
        self.str_to_html_compile = re.compile("|".join(map(re.escape, self.str_to_html_pattern.keys())))

class ErrorMessages:
    ask_check_network = """
AnkiConnect doesn't respond.

Check list
1. Is your Anki running now? your Anki must be running to use AnkiConnect.
2. Is your AnkiConnect plugin installed in your Anki application and enabled?
3. Are an ip and port in option or config files correct?
4. Does your serverside open port?
"""
    connect_time_out = "It's a connection time out."
    unknown_network_error = """It's an unknown error.
Please report it to https://github.com/Constantin1489/trrc/issues"""
    basictype = 'Basic type must have at least two fields'
    wrong_field = '"cannot create note because it is empty"'
    check_notetype = "ERROR: 'def _check_notetype' No predefined notetype is here"
    type_field_suggestion = "suggestion: use --type and --field option."
    read_timed_out = """It's a Read timed out. But it is possible your Anki server is handling
cards now. Within a minute, Your card is maybe available. If you set
to do sync, this program will ignore it by now. Please, sync manually
with '--sync' option without card contents in a command line after a while"""
    valid_api_key_require = "valid api key must be provided. please check " \
            "your apikey and, use --apikey option or add it into a config file."

def error_message_coloring(error_message_string, message_type=None):
    if message_type:
        errormessage = f'{ColorsPrint.FAIL + ColorsPrint.BOLD + message_type + ColorsPrint.ENDC}: {error_message_string}'
    else:
        errormessage =  f'{ColorsPrint.FAIL + ColorsPrint.BOLD + error_message_string + ColorsPrint.ENDC}'
    print(errormessage, file=sys.stderr)

class AnkiConnectInfo:
    """Object contains ip, port, apikey"""

    def __init__(self, web_bind_address='localhost', web_bind_port=8765,
                 apikey=''):
        """TODO: to be defined. """
        self.ip = self._get_ip(web_bind_address)
        self.port = web_bind_port
        self.url = self._get_user_ankiconnect(web_bind_address, web_bind_port)
        self.protocol = self._get_protocol(web_bind_address)
        self.apikey = apikey

    def _get_user_ankiconnect(self, web_bind_address, web_bind_port):

        if web_bind_address.startswith(('http://', 'https://')):
            return f"{web_bind_address}:{web_bind_port}"
        return f"http://{web_bind_address}:{web_bind_port}"

    def _get_ip(self, web_bind_address):
        if web_bind_address.startswith('http://'):
            return web_bind_address[7:]

        if web_bind_address.startswith('https://'):
            return web_bind_address[8:]

        return web_bind_address

    def _get_protocol(self, web_bind_address):
        if web_bind_address.startswith('http://'):
            return 'http'

        if web_bind_address.startswith('https://'):
            return 'https'

        return 'http'

class Card:
    """
    A class for card object
    """

    def __init__(self, deck: str, notetype: str, card_str: str, field: str,
                 cloze_field, cloze_type, ifs='\t'):
        """
        no deck and notetype. because cardlist has deck and notetype.
        """

        self.deck: str = deck
        self.notetype: str = notetype
        self.card_str = card_str
        self.field: str = field
        self.ifs = ifs
        self.cloze_field = cloze_field
        self.cloze_type = cloze_type
        self.content = {}
        self.tag = []

        main_logger.debug('note type: %s, type: %s', self.notetype, type(self.notetype))
        main_logger.debug('IFS: %s, type: %s', ifs, type(ifs))
        main_logger.debug('card object: %s, type: %s', card_str, type(card_str))

    def _check_notetype(self, notetype, splited_card_list: list[str], field: list[str]):
        """
        return card content variables per notetype.
        """

        if field is None:
            if notetype in ['basic', 'Basic']:
                main_logger.debug('hard coded basic is on')
                front = splited_card_list[0]

                try:
                    back = splited_card_list[1]

                # if splited_card_list[1] doesn't exist, then return None.
                except IndexError as exc:
                    main_logger.debug('index error: %s, type: %s',
                                      splited_card_list, type(splited_card_list))
                    raise Exception(ErrorMessages.basictype) from exc

                # tag does not need to be splited
                # suggestion : len(list) condition
                tag = self._is_tag(back, splited_card_list[-1])

                # is it good idea? obj: json
                return { 'Front' : front, 'Back' : back }, tag

            if notetype in ['cloze', 'Cloze']:
                main_logger.debug('cloze is on')
                text = self._cloze_contain_cloze_tag(splited_card_list[0])
                # suggestion : len(list) condition
                try:
                    extra = splited_card_list[1]
                except IndexError:
                    extra = ''

                # in this case, tag will be Text.
                # in this case, parameter should be Text, splited_card_list[-1]

                tag = []
                if text != splited_card_list[-1]:
                # if a record has only Text, then list[-1] is the Text. This cause
                #an error.
                    tag = self._is_tag(extra, splited_card_list[-1])

                return { 'Text' : text, 'Back Extra' : extra }, tag

        # if user defined field exists
        main_logger.debug('field is on')
        if notetype in ['cloze', 'Cloze']:
            if self.cloze_field:
                merged_contents: dict = self._merge_splited_card_list_w_field(self.get_field(self.cloze_field), splited_card_list)

                if ('tag' not in self.get_field(self.cloze_field) and
                    'tags' not in self.get_field(self.cloze_field)):
                    return merged_contents, ['']

            else:
                merged_contents: dict = self._merge_splited_card_list_w_field(field, splited_card_list)

        else:
            merged_contents: dict = self._merge_splited_card_list_w_field(field, splited_card_list)

        if 'tag' not in field and 'tags' not in field:
            return merged_contents, ['']

        # If try-except failed, then spliting self.card_str by IFS is failed.
        # Even if this card failed, it wouldn't break the program but skip to the next card.
        try:
            tag: str = merged_contents.pop('tag')

        except KeyError:
            tag: str = merged_contents.pop('tags')

        tag: list = tag.split(sep=' ')

        return merged_contents, tag

    def _merge_splited_card_list_w_field(self, field: list, card_contents_list: list):

        if len(field) >= len(card_contents_list):
            return dict(zip(field, card_contents_list))
        raise Exception('a number of the fields in the option is ' \
                        'smaller than actual fields of a card content')

    def _is_tag(self, last_item_except_tag, tag_item):
        """
        last card item can not be tag item.
        therefore, if they are the same, there is no tag.
        """

        # This prevent to compare empty tag and last item of cloze.
        # Therefore, cloze can have only one item.
        if tag_item == '':
            return []

        # Last item should not be a tag
        if last_item_except_tag == tag_item:
            return []

        return tag_item.split(' ')

    def _cloze_contain_cloze_tag(self, cloze_content):
        """
        check whether Text contains cloze tag. if not, report and skip.
        """

        if re.search(r'{{c\d+::.*}}', cloze_content):
            return cloze_content

        error_message_coloring(f"{cloze_content} does not have any cloze tag")
        # this break all loops.
        return None


    def make_card(self):
        """
        return final card object to add DB.
        card: tuple[self.content: dict[str, str], self.tag: list[str]]
        """

        try:
            self.content, self.tag = self._check_notetype(self.notetype,
                                                          self.card_str.split(sep=self.ifs),
                                                          self.get_field(self.field))

        except KeyError as err:
            if 'tags' in err.args:
                print(f"ERROR: check your IFS is correct '{self.card_str}' IFS '{self.ifs}'",
                      file=sys.stderr)

    def get_field(self, field):
        if field is None:
            return None
        return field.split(':')

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

    def import_if_file_in_content(self, regex_compile, pattern):

        for key in self.content:
            file_in_field = self.content[key]
            if os.path.isfile(file_in_field):
                main_logger.debug('There is a file to import as a content: %s', file_in_field)
                lines_of_the_file = []
                with open(file_in_field, encoding='utf-8') as f:
                    lines_of_the_file += f.read().splitlines()

                # replace to regexed string
                self.content.update({key :
                                     card_str_regex_substitute('@@@'.join(lines_of_the_file),
                                                               regex_compile,
                                                               pattern)})

def card_str_regex_substitute(str_to_substitute, regex_compile, pattern):

    # For each match, look-up corresponding value in dictionary
    return regex_compile.sub(lambda x: pattern[x.group()], str_to_substitute)
