# apyml
**Under heavy development**

`apyml`- a Machine learning model building tool for humans.


## Requirements

- [Python3.6](https://www.python.org/downloads/release/python-360/)

## Install

```bash
$ python3 setupy.py install --home=$HOME
```

## Usage

```bash
$ python3 -m apyml -h
usage: __main__.py [-h] [-b | -p] filepath

positional arguments:
  filepath       Filepath towards dataset

optional arguments:
  -h, --help     show this help message and exit
  -b, --build    build a model trained with the given data
  -p, --predict  make predictions on given dataset using existing models
  -r, --report   report format
```
