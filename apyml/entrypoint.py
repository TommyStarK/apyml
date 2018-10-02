
from apyml import __version__ as apymlVersion, ExitStatus
from apyml.apyml import APYML

def program(args: dict = None):
    mode, report = None, None

    if not args or not 'filepath' in args:
        raise RuntimeError('Unexpected error occurred.')
    if 'mode' in args:
        mode = args['mode']
    if 'report' in args:
        report = args['report']
    
    app = APYML(args['filepath'], mode=mode, report=report)
    app.run()
    app.report()

def main() -> int:
    try:
        from apyml.cli import parser
        args = vars(parser.parse_args())

        from . import ExitStatus
        exit_status = ExitStatus.OK

        from apyml.context import Context
        Context()

        from apyml.internal.logging import init_logger
        init_logger()
    except KeyboardInterrupt:
        raise
        exit_status = ExitStatus.CTRL_C
    except Exception as e:
        raise
        exit_status = ExitStatus.ERROR
    else:
        try:
            program(args=args)
        except KeyboardInterrupt:
            raise
            exit_status = ExitStatus.CTRL_C
        except Exception as e:
            raise
            exit_status = ExitStatus.ERROR
    return exit_status