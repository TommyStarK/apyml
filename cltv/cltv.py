import argparse

from .internal import Mode

def main():
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
        help='Build CLTV model based on given data',
        action=Mode,
        nargs=0
    )

    group.add_argument(
        '-p',
        '--predict',
        help='Predict CLTV for given data using existing model',
        action=Mode,
        nargs=0
    )

    args = parser.parse_args()
    mode = None if 'mode' not in args else args.mode

    from .internal import init_logger
    init_logger()

    from .context import Context
    Context()

    from .core import Core
    cltv = Core(args.filepath, mode=mode)

    cltv.run()
    cltv.report()
