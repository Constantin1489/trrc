# ToRRential Card processor

* [INTRODUCTION](#introduction)
* [INSTALLATION](#installation)
    * [PIP](#pip)
    * [MANUAL_INSTALLATION](#manual-installation)
* [USAGE](#usage)
* [CONFIG_FILE](#config-file)
* [LOCATIONS](#locations)
* [OPTIONS](#options)
* [FAQ](#faq)
* [CHANGELOG](#changelog)
* [CONTRIBUTION](#contribution)

## INTRODUCTION

**ToRRential Card processor**(**trrc**) is a command-line unix-like program to create anki cards using AnkiConnect plugin.(Think a yt-dlp, but this program is for adding cards into Anki.)

I intent to make it as a Unix-like program. Therefore it **leverages a lot of Unix concepts**.

- It **supports a standard input, PIPE, redirection.** Therefore, you can add bulk cards after mangling your cards with your favorite text editors. With the benefit of unix-like program, you can make a convenient script yourself with your favorite text editors like Vim, Emacs, VScode and so on. See [Usage](#usage)

- It has **shell completions(Zsh, Bash)**.

- It **adds multiple cards at once** using [`--file`](#–file-option) or [PIPE](#pipe) and so on. See [Usage](#usage)

- It also **supports options for ip, port and apikey**. So even some environments you don't want to install Anki, you can add cards if your Anki is running in your home or somewhere, boundlessly.

- It also supports a **rc(config) file** with a alias to reuse options you uses frequently.

- you can **sync Anki** with option `--sync` of **trrc** with or without soon after adding cards.

- It's **user-friendly**. In well-known cases, **trrc** provides solutions. If you
  mistake deck name, it will print all deck name available. If your field is
  wrong, it will print field of the card type used.

```sh
# default card type is 'Basic'
$trrc --field 'fron:bakc:tags' 'What is GPL?	The GNU General Public License is a free, copyleft license for software and other kinds of works.	LICENSE::GPL'
#### Kinds of failures: 1
trrc Tip: --field 'Front:Back:Tags'

You don't have to use all those fields.
For example, if all field of a type is 'Front:Back:Source:Sound:Tags',
you can use only some of them. e.g.: 'Front:Back:Tags'.
####
Total cards: 1 Total fails: 1
```

See [Youtube demonstration video of the author](https://www.youtube.com/watch?v=-3jCwUEAOHE)

***if you decide to use this app, I highly recommend to turn apikey option in your AnkiConnect to prevent malicious attack. (It's not a fault of this app nor AnkiConnect. If the port of AnkiConnect opens without an apikey, anybody can modify your anki deck.)*** See also [AnkiConnect Configure](docs/tips/AnkiConnect_configure/AnkiConnect_addon_configure_example.md)

## INSTALLATION

### pip
`pip install trrc`

### Manual installation
`pip install -r requirements.txt`

`pip install .`

### Install AnkiConnect addon in Anki.

## USAGE
To solve common mistakes, I wrote a lot of examples.

### Standard Input
```sh
# the blank characters except a spacebar in 'Korean Conversation' is a tab.
# the default IFS is a tab.
trrc '안녕	Hello	Korean Conversation'
          # ^         ^
          #tab character

# -F is --IFS. It sets a Internal Field Separator. Mobile devices may not
#support a tab character in their keyboard. In that case, you should use --IFS
#options. (e.g.:-F@)
trrc "back\ttestfront\tvim" -F '\t'

# you can set whatever character you want.
trrc --IFS % '안녕%Hello%Korean'
trrc -F @ '안녕@Hello@Korean'

# you can choose only part of the fields of the card type.
# you can change order of the fields.
trrc --field 'Arbitrary4thField:Arbitrary2ndFieldName:tags' 'FourthContent\tsecondContent\ttag'

# to send your card to other computer(e.g.: ip is 192.168.1.230, port is 4832).
trrc --ip 192.168.1.230 --port 4832 --file Korean_English_conversation.txt
```

#### # To use '\t' as a tab character in an standard input argument, you need to use '$' in front of the string.
```sh
trrc $'안녕\tHello\tKorean'
      ^
```
See also [How to use '\t' in a card content?](#how-to-use-‘%5Ct’-in-a-card-content%3F)

### PIPE

To use PIPE, put `-` in the argument.

```sh
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc -
```

```sh
# bash: \t
echo -e 'basic_type_front_normal_tab with option\tbasic_type_back\tbasic_type_tag' | trrc - -t 'Basic (and reversed card)' --field 'Front:Back:tag'

# bash: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc - -t 'Basic (and reversed card)' --field 'Front:Back:tag'

# zsh: \t
echo 'basic_type_front_normal_tab with option\tbasic_type_back\tbasic_type_tag' | trrc - -t 'Basic (and reversed card)' --field 'Front:Back:tag'

# bash: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc - -t 'Basic (and reversed card)' --field 'Front:Back:tag'

# zsh: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc - -t 'Basic (and reversed card)' --field 'Front:Back:tag'
```

#### PIPE with `cat`

##### example_file_IFS_default.txt
If you use '	'(a tab) as a IFS like a below,
```
#example_file_IFS_deafult.txt
front	back	test
front2	back	test
```
then you don't have to use `--IFS` option.

```sh
cat example_file_IFS_deafult.txt | trrc -
```

##### example_file_IFS_backslash_t.txt
If you use '\t' as a IFS like a below,
```
#example_file_IFS_backslash_t.txt
front\tback\ttest
front2\tback\ttest
```
then use a command like this.

```sh
cat example_file_IFS_backslash_t.txt | trrc - --IFS '\t'
```

#### HEREDOC Standard Input
```sh
trrc --IFS '\t' - <<EOF
front	back	test
front2	back	test
EOF
```

#### HEREDOC PIPE
```sh
cat <<EOF | trrc - --IFS '\t'
front	back	test
front2	back	test
EOF
```

## Config File

*trrc*'s config file extension is `.trrc`.

See [LOCATIONS](#locations) and [How to create a trrc config file](#how-to-create-a-trrc-config-file%3F)

## Locations

By default, *trrc* searches for rc(config) files in directories of the below.
It means if you wrote the config file(only *.trrc*, without any file name.) there,
trrc import the setting in the files if they exists in order.

macOS, Linux:

* `${HOME}/.trrc` # e.g. : `~/.trrc`

* `./.trrc` # working directory.

### Locations: macOS e.g.
* `/Users/username/.trrc`

* If you are in `/Users/username/study/english/`, then also, `/Users/username/study/english/.trrc`

### Locations: Linux e.g.
* `/home/username/.trrc`

* If you are in `/home/username/study/english/`, then also, `/home/username/study/english/.trrc`

## Options

```
usage: trrc [-h] [-D DECK] [-t CARDTYPE] [-i IP] [-p PORT] [-f [FILE ...]]
            [-c FILE] [--alias SECTION] [-F IFS]
            [--field COLON:DELIMITER-SEPARATED:FIELDS]
            [--cloze-field COLON:DELIMITER-SEPARATED:FIELDS]
            [--cloze-type CLOZE_TYPE] [--toml-generate] [--toml-write FILE]
            [--toml-section SECTION] [-H] [--apikey APIKEY] [--sync]
            [--force-add] [--dry-run] [--read-file-in-a-content] [-v]
            [--debug [FILE]] [-V]
            [cardContents ...]

A command-line program to create Anki cards using AnkiConnect API.

positional arguments:
  cardContents          a string divided by IFS. the default IFS is a tab
                        character. instead of a string, It can also take a
                        file consists of strings without '--FILE' option.

options:
  -h, --help            show this help message and exit
  -D DECK, --deck DECK  set a Deck. the default is 'default'.
  -t CARDTYPE, --type CARDTYPE
                        set a card type. the default is 'Basic'.
  -i IP, --ip IP        set a ip that AnkiConnect specified. the default is
                        '127.0.0.1'.
  -p PORT, --port PORT  set a port number that AnkiConnect specified. the
                        default is '8765'.
  -f [FILE ...], --file [FILE ...]
                        set a file that contains card contents.
  -c FILE, --config FILE
                        set a config file to import config options. without
                        this option, this program searches '~/.trrc'.
  --alias SECTION       set a section of a config file to apply options.
                        without this argument, the default is 'default'.
  -F IFS, --IFS IFS     set a delimiter of card contents to use any character
                        other than a tab character. the default is a tab
                        character.
  --field COLON:DELIMITER-SEPARATED:FIELDS
                        set a card field corresponding to the cardContents.
                        the default is 'Front:Back:Tags'.
  --cloze-field COLON:DELIMITER-SEPARATED:FIELDS
                        set a cloze type card field corresponding to the
                        cardContents. The default is 'Text:Back Extra:Tags'.
  --cloze-type CLOZE_TYPE
                        set a type of a fallback for a cloze type. the default
                        is 'cloze'. if user set --field option, then the
                        default won't work. even a string contains cloze, the
                        program will process as a field unless user set
                        --cloze-type
  --toml-generate       print toml configs with current arguments. to set a
                        section of it, use it with '--toml-section' option.
  --toml-write FILE     write a config file with options used. to set a
                        section, use '--toml-section'.
  --toml-section SECTION
                        set a toml section. the default is 'untitled'.
  -H, --render-HTML     set to allow to render a HTML tag. the default doesn't
                        allow render a HTML tag, therefore <br> won't be a new
                        line.
  --apikey APIKEY       set an api key for AnkiConnect. if it is specified,
                        --debug options will mask it because of security
                        concern.
  --sync                sync Anki. if there is a card to process, trrc syncs
                        after adding the card. the default is not to sync.
  --force-add           create a card even if there is a duplicate in the
                        deck.
  --dry-run             perform a trial run without sending to Anki.
  --read-file-in-a-content
                        set to allow to replace a file in contents with its
                        contents. a default setting doesn't read it
  -v, --verbose         print a card being currently processed.
  --debug [FILE]        print debug information. if you specify FILE, trrc
                        writes debug there.
  -V, --version         print a version number and a license of trrc.
```

### --file option

#### examplefile.txt
This is an example which trrc takes. IFS is a tab which is a default IFS.

```
Anki	Anki is a free and open-source flashcard program using spaced repetition	anki
To make a log message in python, What library Should I use?	logging	python::library
```
* `trrc --file examplefile.txt`


### --read-file-in-a-content
Let's say you are learning Rust Language.
Save this statements in a text file called 'rust_hello.txt'
```rust
fn main() {
        println!("Hello, world!");
}
```

and create a card with `--read-file-in-a-content` option

```sh
trrc '[Rust] print "Hello, world!"	rust_hello.txt	rust::println' --read-file-in-a-content
```

trrc will read the file 'rust_hello.txt' and use it as a content.
## FAQ

### How to add several tags?

A tag is a word. Therefore a spacebar will separate tags.

So for example, (IFS of tags is a tab character as a default.): `CS linux::http linux::network`

```sh
trrc '[linux] port 80	HTTP's port	CS linux::http linux::network'
```

trrc will interpret `CS linux::http linux::network` as a list which is `['CS', 'linux::http', 'linux::network']`

### How to create a trrc config file?

create config file with `.trrc` extension.

Let's say your previous command was
```sh
trrc -F@ --type 'Basic' --ip 127.0.0.1 --field 'Front:Back:Tags' --deck 'Computer Science' 'What is GPL?@The GNU General Public License is a free, copyleft license for software and other kinds of works.@LICENSE::GPL'
```

Before creating a default config file, you should check the config.

So, add `--toml-generate` to print configs.

Also, set a section name with `--toml-section SECTION`

e.g.:
```sh
trrc -F@ --type 'Basic' --ip 127.0.0.1 --field 'Front:Back:Tags' --deck 'Computer Science' 'What is GPL?@The GNU General Public License is a free, copyleft license for software and other kinds of works.@LICENSE::GPL' --toml-generate --toml-section 'CS'

```
***But if you want to use the config as a default, then `--toml-section 'default'`***

trrc will print,
```sh
[CS]
deck = "Computer Science"
cardtype = "Basic"
ip = "127.0.0.1"
ifs = "@"
field = "Front:Back:Tags"
```

If there is nothing wrong, copy the text and paste to `~/.trrc`
or use `--toml-write`

```sh
trrc -F@ --type 'Basic' --ip 127.0.0.1 --field 'Front:Back:Tags' --deck 'Computer Science' 'What is GPL?@The GNU General Public License is a free, copyleft license for software and other kinds of works.@LICENSE::GPL' --toml-section 'CS' --toml-write ~/.trrc
```
And you can reuse your config with `--alias CS`.


Also you can overwrite the config with an argument,
```sh
--alias CS --IFS ^
```
It will use CS config but IFS is '^'.

### How to reuse the specific config?

If your config file has 'CS' section, the append `--alias 'CS'` in your command.

### Tip for writing your own script.

In the case with your own script, for a backup purpose, I recommend to create a temp file to use `--file` option or PIPE.

Avoid to use the modules of the library directly because it's alpha version.

This program's License is GPL3. See [License](LICENSE).

If you need to submit your code using trrc, discuss with the person concerned about the license.

### How to use '\t' in a card content?

Yes, It's possible to interpret `\t` as a tab. But in a default '	'(tab) IFS,
the shell behavior that doesn't interpret '\t' as a tab character is a normal
behavior, therefore if you add a card using '\t' as a IFS in a standard
input, you need to use `--IFS '\t'` or put `$` in front of single qoute.
- [ ] add detailed explanation.

```sh
set -x
echo 'front	back	test'
echo 'front\tback\ttest'
echo $'front\tback\ttest'
set +x
```

### How to add a new line?

Use `\n` to make a new line.
```
trrc 'First line\nSecond line	back	tag'
```

### How to open a port?

Basically, when you are running anki with an AnkiConnect addon, the port(default is 8765) of AnkiConnect opens.

But if your want to send a card using **trrc** from outside of your computer which is running Anki with AnkiConnect, you may need to modify firewall option on the computer or a router.

### How to make iOS shortcuts with **trrc**

See [iOS_shortcuts_example](docs/tips/iOS_shortcuts_setting_example/iOS_shortcuts_example.md)

## Changelog

| Version | Note                     | 
|:--------|:-------------------------|
| HEAD    | add shell completion. | 
| 0.1.2    | fix sync option error handle. | 
| 0.1.1   | init                     | 

## Contribution

Thank you for letting me know the bug! Please report the bug in [issue tracker](https://github.com/Constantin1489/trrc/issues).

Personally I like this app as a method to add cards and use daily, so I will keep developing it. Because I'm trying to get a job, an update delivery can be slow. But after getting a job, I will learn some good clean code conventions and apply it.

Currently I'm writing tests to guarantee a basic functionality, documents and comments on codes.

Also there won't be massive changes for a while. Because I think I should
redesign the program for scalability. Think about making card from 'git-diff'. To make such functions quickly I need to redesign.

If there is changes, I'll write how it changes, examples on how to change your codes.

I'm happy to accept criticism, PR, and so on.

There are a lot of grammar mistakes. English is not my language. Catch! PR! PLEASE!

If you're good at unix, linux, or shell, please enlighten me! I really want to hear about book recomendations, cli program to benchmark and so on.

## TODO

- [ ] remove dependency: requests lib.
- [ ] windows support.
    - py2exe
    - file path (e.g.: default config file)
- [ ] send media files directly to Anki.
- [ ] create card from git-diff, git-show
    - option: --mode=git --header 'Optimize logging message\n		'
    - without --header, use git commit message as header.
- [ ] support markdown, mad type and so on.
    - --vertical?
    - Pseudo HEREDOC mode.
- [ ] get fields of a deck.
    - error handle.
- [ ] support shell environment variable.
    - prefix: TRRC
    - e.g.: TRRC_deck, TRRC_tag: global tag
- [ ] new verbose purpose.
    - -v : stdout, other logging format.
- [ ] add reliable and insightful pytests
- [x] config file option
- [x] HTML interpret on-off mode.
    - [x] \<br\> &lt, &gt & HTML on <-> HTML off and `\n`
        - [x] First, change every HTML tags to &gt &lt. then change \n to <br>
    - [x] should it be a HTML off mode a default?
- [ ] Embedding modules: allow trrc as a module to use in python script.
- [x] Error message: file doesn't exist.
- [x] search rc file in the working directory.
- [ ] use # comment in a file as a temporary card option or method switcher.
    - [ ] Allow adding card vertically
        - [ ] #NEW FRONT(field)
        - [ ] #DONE TAGS
    - [ ] change option with # -F%
        - [ ] back to option of stdin
