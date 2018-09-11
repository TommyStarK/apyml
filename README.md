# cltv-predict
**Under heavy development**

`cltv-predict` is the first attempt of writting a tool capable of
adapting to the structure and shape of a given dataframe and build
a customer lifetime value predictive model based on xgboost.

With the proper configuration, the app is able to follow specific data
preprocessing guidelines and build any kind of model from the simplest
to highly complex.

This tool has been designed for being easily customizable.

## Usage

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

## Build configuration

 - Required Configuration

    Inc

 - Data preprocessing guidelines

    Inc


## How to use my predictive models ?

  Inc



