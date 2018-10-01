import argparse

from apyml.internal import Mode

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


# from .internal import Mode

# def main():
    

#     args = parser.parse_args()
#     mode = None if 'mode' not in args else args.mode

#     print(args)

#     from .internal import init_logger
#     init_logger()

#     from .context import Context
#     Context()

#     from .apyml import APYML
#     apyml = APYML(args.filepath, mode=mode, report=args.report)

#     apyml.run()
#     apyml.report()
