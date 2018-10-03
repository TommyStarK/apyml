import json
import os

from apyml import ColorStatus
from apyml.internal import info, fatal
from apyml.internal.metaclass import Singleton

class Context(metaclass=Singleton):
    def __init__(self):
        self._config = {}
        self._context = {}
        self._path_to_directives = 'apyml.directives.directives'
        self._path_to_store = 'apyml/models'
        self._store = {}

        with open('config.json') as f:
            self._config = json.load(f)

        for root, dirs, files in os.walk(self._path_to_store):
            for subdir in dirs:
                self._store[os.path.join(root, subdir)] = []
            self._store[root] = files

    def get_from_config(self, target) -> dict:
        keys = []
        if isinstance(target, str):
            keys = [target]
        elif isinstance(target, list):
            keys = target
        else:
            raise ValueError('Context.get_from_config: param must be either a string or a list.')

        body = []
        for k in keys:
            tmp = {}
            if isinstance(self._config[k], list):
                tmp = {k: [dict(**i)] for i in self._config[k]}
            else:
                tmp = dict(**self._config[k])
            body.append(tmp)

        return {k: v for i in body for k, v in i.items()}

    def get_directives_path(self) -> str:
        return self._path_to_directives

    def get_store_path(self) -> str:
        return self._path_to_store

    def get(self, key: str) -> object:
        return self._context.get(key, None)

    def set(self, key: str, item: object):
        self._context[key] = item