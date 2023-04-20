# AnkiAdderAll

* [INTRODUCTION](#introduction)
* [INSTALLATION](#installation)
    * [PIP](#pip)
    * [MANUAL_INSTALLATION](#manual-installation)

## INTRODUCTION

ankiadderall is a command line application to create anki cards. 

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
a tag is a word. therefore a spacebar will separate tags.
Ankiadderall will interpret `Linux::kickstart Linux::vm` as a list which contains ['Linux::kickstart', 'Linux::vm']

### How to add a new line?

\<br\> is a new line. It's because anki or ankiadderall interprets contents of a card as a HTML. Currently I'm working on it. 

## TODO

* [ ] add reliable and insightful pytests
* [ ] config file option
* [ ] HTML interpret on-off mode.
    * [ ] \<br\> &lt, &gt & HTML on <-> HTML off and `\n`
    * [ ] should it be a HTML off mode a default?
* [ ] Embedding modules: allow ankiadderall as a module to use in python script.
* [ ] Error message: file doesn't exist. (if stdin file without option, then ...)
    * python /Users/constantinhong/TODO/ankiadderall/ankiadderall/addstring.py /Users/constantinhong/TODO/tempfile_dir/snippet.2Tw9DzvZ.ExportedCard
    * ERROR TEMP raise!!!!!!!!DO/tempfile_dir/snippet.2Tw9DzvZ.ExportedCard
