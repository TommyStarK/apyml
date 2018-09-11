# cltv-predict

# Usage

```bash
# install package
$ pip install -e .

# use package
$ python3 -m cltv -h
usage: __main__.py [-h] [-b | -p] filepath

positional arguments:
  filepath       Filepath or S3 url towards targeted data

optional arguments:
  -h, --help     show this help message and exit
  -b, --build    Build CLTV model based on given data
  -p, --predict  Predict CLTV for given data using existing models
```

# How to configure the app

Inc
