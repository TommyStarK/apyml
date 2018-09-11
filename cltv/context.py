import json
import os

from .internal import info
from .internal import Singleton

class Context(metaclass=Singleton):
    def __init__(self):
        self._root = 'cltv/models'
        self._load_config()
        self._load_models()
        info('Context initialization [\033[0;32mOK\033[0m]')

    def _load_config(self):
        with open('config.json') as f:
            self._config = json.load(f)
            if not self._config:
                import sys
                from .internal import fatal
                fatal('Initialization context [\033[0;31mFAILED\033[0m]')
                sys.exit(1)

    def _load_models(self):
        self._store = {}
        for root, dirs, files in os.walk(self._root):
            for subdir in dirs:
                self._store[os.path.join(root, subdir)] = []
            self._store[root] = files

    def get_config(self, key: str) -> dict:
        return dict(**self._config[key])

    def get_store(self) -> dict:
        return self._store
