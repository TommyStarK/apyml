import argparse

from apyml.internal.mode import Mode

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

parser.add_argument(
    'filepath',
    type=str,
    help='Filepath or S3 url towards targeted data'
)

group.add_argument(
    '-b',
    '--build',
    help='build a model trained with the given data',
    action=Mode,
    nargs=0
)

group.add_argument(
    '-p',
    '--predict',
    help='make predictions on given dataset using existing models',
    action=Mode,
    nargs=0
)

parser.add_argument(
    '-r',
    '--report',
    type=str,
    help='report format'
)