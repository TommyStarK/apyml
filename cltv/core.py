import sys

from multiprocessing import Pool

from .context import Context
from .dataframe import Framator
from .dataframe import Preprocessor
from .internal import Filepath
from .internal import merkle_root
from .internal import fatal
from .internal import info

context = Context()

class Core(object):
    def __init__(self, datapath: str, mode: str = None):
        self.dataframe = None
        self.datapath = datapath
        self.handler = { 'build': self._build, 'predict': self._predict }
        if not mode:
            self.mode = 'predict'
        else:
            self.mode = mode

        try:
            self.infos = Filepath(datapath).get_infos()
            self.dataframe = Framator(self.infos).create_dataframe()
            print(self.dataframe.describe())
            print(self.dataframe.head())
            info('Dataframe creation [\033[0;32mOK\033[0m]')
            self.dataframe = Preprocessor(self.dataframe).preprocess()
            info('Data preprocessing [\033[0;32mOK\033[0m]')
            self.dataframe_hash = merkle_root(list(self.dataframe.columns.values))
            info(f"Dataframe shape: [{self.dataframe.shape[0]} rows x {self.dataframe.shape[1]} columns] hash: {self.dataframe_hash}")
            info(f"CLTV Core initialization [\033[0;32mOK\033[0m]")
        except Exception as e:
            fatal('CLTV Core initialization [\033[0;31mFAILED\033[0m]')
            fatal(e)
            sys.exit(1)

    def _build(self):
        self.config = context.get_config('build')
        print(self.config)
        print(self.dataframe.head())
        try:
            pass
        except Exception as e:
            pass

    def _predict_routine(self, path: str, models: list):
        print(path, models)
        tmp = self.dataframe.copy()
        print(tmp.head())


    def _predict(self):
        self.config = context.get_config('predict')

        try:
            store = context.get_store()
            pool = Pool(processes=len(self.config['targets']))
            pool.starmap(self._predict_routine, [(path, models) for path, models in self._retrieve_valid_model(store)])
            pool.close()
            pool.join()
        except Exception as e:
            fatal(e)
            sys.exit(1)

    def _retrieve_valid_model(self, store: dict) -> tuple:
        for target in self.config['targets']:
            for k, v in store.items():
                if k.find(target) > -1:
                    yield (k, v)

    def report(self):
        info('CLTV writing report to disk...')

    def run(self):
        self.handler[self.mode]()
