"""The main entry point. Invoke as `apyml' or `python -m apyml'.
"""
import sys

def main():
    try:
        from apyml.entrypoint import main
        sys.exit(main())
    except KeyboardInterrupt:
        from apyml import ExitStatus
        sys.exit(ExitStatus.CTRL_C)


if __name__ == '__main__':
    main()