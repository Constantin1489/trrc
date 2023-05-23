# ToRRential Card processor

* [INTRODUCTION](#introduction)
* [INSTALLATION](#installation)
    * [PIP](#pip)
    * [MANUAL_INSTALLATION](#manual-installation)

## INTRODUCTION

**ToRRential Card processor**(**TRRC**) is a command line unix application to create anki cards using AnkiConnect plugin.(Think a yt-dlp, but this application is for adding cards into Anki.)

I intent to make it as a Unix-like application. Therefore it **leverages a lot of Unix concepts**.

- it **supports a standard input, pipe, redirection.** Therefore, you can add bulk cards after mangling your cards with your favorite text editors. With the benefit of Unix-like application, with basic shell script, you can make convenient simple card adding script yourself with your favorite text editors like Vim, Emacs, VScode and so on.

- It also **supports options for ip, port and apikey**. So even some environments you don't want to install Anki, you can add cards if your Anki is running in your home or somewhere, boundlessly.

- It also supports a **rc(or config) file** with a alias to reuse options you uses frequently.

- you can **sync Anki** with option `--sync` of **trrc** with or without soon after adding cards.

So you can add your card at any circumstance conveniently.

***if you decide to use this app, I highly recommend to turn apikey option in your AnkiConnect to prevent malicious attack. (It's not a fault of this app nor AnkiConnect. If the port of AnkiConnect opens without an apikey, anybody can modify your anki deck.)***

## INSTALLATION

### pip
`pip install trrc`

### Manual installation
`pip install -r requirements.txt`
`pip install .`

## USAGE
I wrote a lot of examples.

### Standard Input
```sh
trrc '안녕	Hello	Korean Conversation'
trrc $'안녕\tHello\tKorean'
trrc "back\ttestfront\tvim" -F '\t'
trrc --IFS % '안녕%Hello%Korean'
trrc --column 'ArbitraryFourthFieldName:ArbitrarysecondFieldName:tag' 'FourthContent\tsecondContent\ttag'
trrc --ip 192.168.1.230 --port 4832 --debug --file Korean_English_conversation.txt
```

### Pipe Redirection
```sh
# bash: \t
echo -e 'basic_type_front_normal_tab with option\tbasic_type_back\tbasic_type_tag' | trrc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

# bash: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

# zsh: \t
echo 'basic_type_front_normal_tab with option\tbasic_type_back\tbasic_type_tag' | trrc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

# zsh: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug
```

### --file option

#### examplefile.txt
```
Anki	Anki is a free and open-source flashcard program using spaced repetition	anki
```
* `trrc --file examplefile.txt`

## Locations

*TRRC* searches for rc(or config) files in the user's home directory:

macOS, Linux:
    * `$(HOME)/.trrc`

## FAQ

### How to add several tags?

a tag is a word. Therefore a spacebar will separate tags.

So for example, (IFS is a tab character as a default.): `linux::http linux::network`

```
trrc '[linux] port 80	HTTP's port	linux::http linux::network'
```
TRRC will interpret`linux::http linux::network` as a list which is `['linux::http', 'linux::network']`

### How to add a new line?

Use `\n` to make a new line.
`First line\nSecond line	back	tag`

### How to open a port?

Basically, when you are running anki with an AnkiConnect addon, the port(default is 8765) of AnkiConnect opens.

But if your want to send a card using **trrc** from outside of your computer which is running Anki with AnkiConnect, you may need to modify firewall option on the computer.

### This software misses some characters.

Thank you for letting me know! Please report the bug in [issue tracker](https://github.com/Constantin1489/ankistreamadd/issues).

## TODO

- [x] verbose option
    - [x] Is verbose critical or info.
    - [x] if (verbose and debug), debug overwrites verbose. or other algo
        - [x] if debug:; elif verbose:; else; return None
- [ ] new verbose purpose.
- [ ] add reliable and insightful pytests
- [x] config file option
- [x] HTML interpret on-off mode.
    - [x] \<br\> &lt, &gt & HTML on <-> HTML off and `\n`
        - [x] First, change every HTML tags to &gt &lt. then change \n to <br>
    - [x] should it be a HTML off mode a default?
- [ ] Embedding modules: allow TRRC as a module to use in python script.
- [x] Error message: file doesn't exist.
- [ ] search rc file in the working directory.
- [ ] use # comment in a file as a temporary card option or method switcher.
    - [ ] Allow adding card vertically
        - [ ] #NEW FRONT(field)
        - [ ] #DONE TAGS
    - [ ] change option with # -F%
        - [ ] back to option of stdin
