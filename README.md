# dump_github_repository

## Usage : dump all of hidenorly's repositories

```
% python3 dump_github_repository.py hidenorly
```

## Usage : dump all of hidenorly's repositories as git clone manner

```
% python3 dump_github_repository.py hidenorly --mode=clone
```


## Usage : dump all of hidenorly's repositories of Ruby based

```
% python3 dump_github_repository.py hidenorly --filterLang="Ruby"
```

## Usage : dump all of hidenorly's repositories of --filterRepo matched

```
% python3 dump_github_repository.py --filterRepo="rst.*" hidenorly
  "rst_opt_parse":{"url":"https://github.com//hidenorly/rst_opt_parse", "lang":"Rust"}",
  "rst_task_manager":{"url":"https://github.com//hidenorly/rst_task_manager", "lang":"Rust"}",
  "rst_string_tokenizer":{"url":"https://github.com//hidenorly/rst_string_tokenizer", "lang":"Rust"}",
```


# TODO

* [done] Add parsing github's repositories
* [done] Add multiple account support
* [done] Add --mode=dump,clone support
* [done] Add --filterLang support
* [done] Add --filterRepo support

