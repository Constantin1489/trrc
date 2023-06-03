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

- It also supports a **rc(config) file** with a alias to reuse options you uses frequently.

- you can **sync Anki** with option `--sync` of **trrc** with or without soon after adding cards.

So you can add your card at any circumstance conveniently.

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
# the black characters except a spacebar in 'Korean Conversation' is a tab.
# the default IFS is a tab.
trrc '안녕	Hello	Korean Conversation'

# -F is --IFS. It sets a Internal Field Separator. Mobile devices may nott
support a tab character in their keyboard. In that case, you should use --IFS
options.
trrc "back\ttestfront\tvim" -F '\t'

# you can set whatever character you want.
trrc --IFS % '안녕%Hello%Korean'
trrc -F % '안녕%Hello%Korean'

# you can choose only part of the fields of the card type.
# you  can change order of the fields.
trrc --field 'Arbitrary4thField:Arbitrary2ndFieldName:tags' 'FourthContent\tsecondContent\ttag'

# to send your card to other computer(e.g.: ip is 192.168.1.230, port is 4832).
trrc --ip 192.168.1.230 --port 4832 --file Korean_English_conversation.txt
```

#### # To use '\t' as a tab character in an standard input argument, you need to use '$' in front of the string.
```sh
trrc $'안녕\tHello\tKorean'
      ^
```
Check this: [How to use '\t' in a card content?](#how-to-use-‘%5Ct’-in-a-card-content%3F)

### PIPE

To use PIPE, put `-` in the argument.

```sh
echo 'basic_type_front_normal_tab with option	basic_type_back	basic_type_tag' | trrc -
                                                                                       ^
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

## config file

*TRRC*'s config file extension is `.trrc`.

See [LOCATIONS](#locations) and [How to create a trrc config file](#how-to-create-a-trrc-config-file%3F)

## Options
### --file option

#### examplefile.txt
This is an example which trrc takes. IFS is a tab which is a default IFS.

```
Anki	Anki is a free and open-source flashcard program using spaced repetition	anki
To make  a log message in python, What library Should I use?	logging	python::library
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

## Locations

By default, *TRRC* searches for rc(config) files in directories of the below.
It means if you wrote the config file(only *.trrc*, without any file name.) there,
trrc import the setting in the files if they exists in order.

macOS, Linux:

* `$(HOME)/.trrc` # e.g. : `~/.trrc`

* `./.trrc` # working directory.

### Locations: macOS e.g.
* `/Users/username/.trrc`

* If you are in `/Users/username/study/english/`, then also, `/Users/username/study/english/.trrc`

### Locations: Linux e.g.
* `/home/username/.trrc`

* If you are in `/home/username/study/english/`, then also, `/home/username/study/english/.trrc`

## FAQ

### How to add several tags?

A tag is a word. Therefore a spacebar will separate tags.

So for example, (IFS of tags is a tab character as a default.): `CS linux::http linux::network`

```sh
trrc '[linux] port 80	HTTP's port	CS linux::http linux::network'
```

TRRC will interpret `CS linux::http linux::network` as a list which is `['CS', 'linux::http', 'linux::network']`

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

And you can reuse your config with `--alias CS`

Also you can overwrite the config with an argument,
```sh
--alias CS --IFS ^
```
It will use CS config but IFS is '^'.

### Tip for writing your own script.
***In the case with your own script, for a backup purpose, I recommend to create a temp file to use `--file` option or PIPE.***

### How to use '\t' in a card content?

Yes, It's possible to interpret `\t` as a tab.
But in a default '	'(tab) IFS, to shell behavior is a normal behavior,
therefore if you add a card(s) using '\t' as a IFS in a standard input, you need
to use `--IFS '\t'` or put `$` in front of single qoute.
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
`First line\nSecond line	back	tag`

### How to open a port?

Basically, when you are running anki with an AnkiConnect addon, the port(default is 8765) of AnkiConnect opens.

But if your want to send a card using **trrc** from outside of your computer which is running Anki with AnkiConnect, you may need to modify firewall option on the computer or a router.

* #### RHEL (fedora, cent, rocky, alma)
- [ ] add port open explanation.

* #### Ubuntu
- [ ] add port open explanation.

* #### macOS
- [ ] add port open explanation.

* #### router
Google 'YOUR_ROUTER_NAME port forwarding'

### This software misses some characters.

Thank you for letting me know! Please report the bug in [issue tracker](https://github.com/Constantin1489/ankistreamadd/issues).

## Development Plan

Personally I like this app as a method to add cards and use daily, so I will keep developing it. Because I'm trying to get a job, an update delivery can be slow. But after getting a job, I will learn some good clean code conventions and apply it.

Currently I'm writing tests to guarantee a basic functionality, documents and comments on codes.

Also there is no massive changes by now. If there is, I'll write how it changes, examples on how to change your codes.

I'm happy to accept criticism, PR, and so on.

If you're good at unix, linux, or shell, please enlighten me! I really want to hear about book recomendations, cli application to benchmark and so on.

## TODO

- [ ] send media files directly to Anki.
- [ ] get fields of a deck.
- [ ] check whether your cards good to send.
- [ ] support shell environment variable.
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
