"""
apyml - a Machine learning model building tool for humans.
"""
__version__ = '1.0.0-dev'
__author__ = 'TommyStarK <Thomas Milox>'
__licence__ = 'MIT'


class ExitStatus:
    OK = 0
    ERROR = 1
    CTRL_C = 130

class ColorStatus:
    SUCCESS = '\033[0;32mok\033[0m'
    FAILURE = '\033[0;31mfailure\033[0m'