# AnkiAdderAll

* [INTRODUCTION](#introduction)
* [INSTALLATION](#installation)
    * [PIP](#pip)
    * [MANUAL_INSTALLATION](#manual-installation)

## INTRODUCTION

Ankiadderall is a command line unix application to create anki cards using AnkiConnect plugin.(Think a yt-dlp, but It's for adding cards into Anki.)

I intent to make it as a Unix-like application. Therefore it leverages a lot of concepts.

- it **supports our favorite a standard input and pipe redirection.**. Therefore, you can add bulk cards after mangling your cards with your favorite text editors. With the benefit of Unix-like application, with basic shell script, you can make convenient simple card adding script yourself with your favorite text editors like Vim, Emacs, VScode and so on.

- It also **support to change ip, port and apikey by options**. So even some environments you don't want to install Anki, you can add cards if your Anki is running in your home or somewhere, boundlessly.

- It also supports a **rc(or config) file** with a alias to reuse options you uses frequently.

- you can **sync anki** with option `--sync`, also even soon after adding cards.

So you can add your card at any circumstance conveniently.

***if you decide to use this app, I highly recommend to turn apikey option in your AnkiConnect to prevent malicious attack. (It's not a fault of this app. If AnkiConnect port open without an apikey, anybody can modify your anki deck.)***

## INSTALLATION

### pip
`pip install ankiadderall`

### manual installation
`pip install -r requirements.txt`

## USAGE
The usage should be pretty self-explanatory. But to solve common mistakes, I wrote a lot of examples. Before post an issue, compare your command with below, please.

### stdin
```python3
pourc '안녕	Hello	Korean Conversation'
pourc $'안녕\tHello\tKorean'
../ankiadderall/addstring.py "back\ttestfront\tvim" -F '\t'
pourc --IFS % '안녕%Hello%Korean'
pourc --column 'ArbitraryFourthFieldName:ArbitrarysecondFieldName:tag' 'FourthContent\tsecondContent\ttag'
pourc --ip 192.168.1.230 --port 4832 --debug --file Korean_English_conversation.txt
```

### pipe redirection
```python3
# bash: \t
echo -e 'basic_type_front_normal_tab with option\tbasic_type_back\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

# bash: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

# zsh: \t
echo 'basic_type_front_normal_tab with option\tbasic_type_back\tbasic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug

# zsh: using a tab
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | pourc -t 'Basic (and reversed card)' --column 'Front:Back:tag' --debug
```

### --file option

#### examplefile.txt
```
Anki	Anki is a free and open-source flashcard program using spaced repetition	anki
```
* `pourc --file examplefile.txt`


## FAQ

### How to add several tags?
a tag is a word. Therefore a spacebar will separate tags.

So for example, (IFS is a tab character as a default.): `linux::http linux::network`

```
pourc '[linux] port 80	HTTP's port	linux::http linux::network'
```
Ankiadderall will interpret`linux::http linux::network` as a list which is `['linux::http', 'linux::network']`

### How to add a new line?

\<br\> is a new line. It's because anki or ankiadderall interprets contents of a card as a HTML. Currently I'm working on it. 

### How to open a port?

Basically, when you are running anki with an AnkiConnect addon, the port(default is 8765) of AnkiConnect opens.

But if your want to send a card by pourc from outside of your computer, you need to modify firewall option.

### This software misses some characters.

Thank you for letting me know! Please report the bug.

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
- [ ] Embedding modules: allow ankiadderall as a module to use in python script.
- [x] Error message: file doesn't exist.
- [ ] use # comment in a file as a temporary card option or method switcher.
    - [ ] Allow adding card vertically
        - [ ] #NEW FRONT(field)
        - [ ] #DONE TAGS
    - [ ] change option with # -F%
        - [ ] back to option of stdin
