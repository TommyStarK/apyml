"""The program main function.
"""

from apyml import __version__ as apymlVersion, ExitStatus, ColorStatus
from apyml.apyml import APYML
from apyml.internal import info, fatal

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
        from . import ExitStatus
        exit_status = ExitStatus.OK

        from apyml.cli import parser
        args = vars(parser.parse_args())

        from apyml.internal.logging import init_logger
        init_logger()

        from apyml.context import Context
        Context()
        info(f'Context creation [{ColorStatus.SUCCESS}]')
    except KeyboardInterrupt:
        info('Keyboard interruption (ctrl+c).')
        exit_status = ExitStatus.CTRL_C
        raise
    except Exception as e:
        fatal(f'Core initialization [{ColorStatus.FAILURE}]')
        fatal(e)
        exit_status = ExitStatus.ERROR
        raise
    else:
        try:
            program(args=args)
        except KeyboardInterrupt:
            info('Keyboard interruption (ctrl+c).')
            exit_status = ExitStatus.CTRL_C
            raise
        except Exception as e:
            fatal(e)
            exit_status = ExitStatus.ERROR
            raise
    return exit_status