import json
import os

from apyml.internal import *
from apyml.internal.metaclass import Singleton

class Context(metaclass=Singleton):
    def __init__(self):
        self._root = 'apyml/models'
        self._directives = 'apyml.directives.directives'
        self._context = {}
        self._load_config()
        self._load_models()
        info('Context initialization [\033[0;32mOK\033[0m]')

    def _load_config(self):
        with open('config.json') as f:
            self._config = json.load(f)
            if not self._config:
                from apyml.internal import fatal
                fatal('Initialization context [\033[0;31mFAILED\033[0m]')
                raise RuntimeError('Unexpected error occurred during the loading of the configuration.')

    def _load_models(self):
        self._store = {}
        for root, dirs, files in os.walk(self._root):
            for subdir in dirs:
                self._store[os.path.join(root, subdir)] = []
            self._store[root] = files

    def get_config(self, key: str) -> dict:
        if isinstance(self._config[key], list):
            return {key: [dict(**tmp)] for tmp in self._config[key]}
        return dict(**self._config[key])

    def get_store(self) -> dict:
        return self._store
    
    def get_directives(self) -> str:
        return self._directives

    def get_store_root(self) -> str:
        return self._root

    def set_to_context(self, key: str, item: object):
        self._context[key] = item

    def get_from_context(self, key: str) -> object:
        return self._context[key]
