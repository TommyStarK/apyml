from multiprocessing import Pool

from apyml.core import Framator
from apyml.core import Preprocess
from apyml.context import Context
from apyml.internal import Filepath
from apyml.internal import merkle_root
from apyml.internal import fatal
from apyml.internal import info

context = Context()

class APYML(object):
    def __init__(self, datapath: str, mode: str = None, report: str = None):
        self._dataframe = None
        self._datapath = datapath
        self._mode = 'predict' if not mode else mode
        # self._objective = { 
        #     'build': self._build, 
        #     'predict': self._predict 
        # }

    
    def run(self):
        Preprocess()


    # def _init_build(self, predict: bool = False):
    #     try:
    #         self.infos = Filepath(self._datapath).get_infos()
    #         self._dataframe = Framator(self.infos).create_dataframe()
    #         info('Dataframe creation [\033[0;32mOK\033[0m]')
    #         self._dataframe = Preprocess(self._dataframe, predict=predict)
    #         info('Data preprocessing [\033[0;32mOK\033[0m]')
    #         info('APYML initialization [\033[0;32mOK\033[0m]')
    #     except Exception as e:
    #         fatal('APYML initialization [\033[0;31mFAILED\033[0m]')
    #         fatal(e)
    #         raise

    # def _build(self):
    #     try:
    #         import pickle
    #         self._init_build()
    #         from apyml.core import build
    #         for directive, model in build(self._dataframe):
    #             h = context.get_from_context(f'{directive}-dataframe_hash')
    #             pickle.dump(model, open(f"{context.get_store_root()}/{directive}/{h}", 'wb'))
    #     except Exception as e:
    #         raise e

    # def _predict_routine(self, path: str, models: list):
    #     from apyml.internal import merkle_root
    #     h = merkle_root(self._dataframe.columns)
    #     print(h)
    #     if h not in models:
    #         raise RuntimeError('No model found for this kind of dataframe')
    #     target = models[models.index(h)]
    #     import pickle
    #     model = pickle.load(open(f'{path}/{target}', 'rb'))
    #     self._preds = model.predict(self._dataframe)
    #     print(self._preds)


    # def _predict(self):
    #     self.config = context.get_config('predict')

    #     try:
    #         store = context.get_store()
    #         self._init_build(predict=True)
    #         pool = Pool(processes=len(self.config['targets']))
    #         pool.starmap(self._predict_routine, [(path, models) for path, models in self._retrieve_valid_model(store)])
    #         pool.close()
    #         pool.join()
    #     except Exception as e:
    #         fatal(e)
    #         sys.exit(1)

    # def _retrieve_valid_model(self, store: dict) -> tuple:
    #     for target in self.config['targets']:
    #         for k, v in store.items():
    #             if k.find(target) > -1:
    #                 yield (k, v)

    def report(self):
        info('APYML writing report to disk...')

    # def run(self):
    #     self._handler[self._mode]()
