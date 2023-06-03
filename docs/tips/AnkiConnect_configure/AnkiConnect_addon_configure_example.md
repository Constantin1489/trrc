To protect your Anki,

You need to set AnkiConnect apikey like this.
Change 'THIS_IS_THE_APIKEY' to other words.

```
{
    "apiKey": "THIS_IS_THE_APIKEY",
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "0.0.0.0",
    "webBindPort": 8765,
    "webCorsOriginList": [
        "http://localhost"
    ]
}
```

In this case, to use `--apikey` of trrc,

```sh
trrc --apikey 'THIS_IS_THE_APIKEY' 'front card	back card	test'
```

To use the `--apikey` by default config,
```sh
trrc --apikey 'THIS_IS_THE_APIKEY' --toml-generate
```

Copy and paste the result into the config file(e.g.: ~/.trrc).
