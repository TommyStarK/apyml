from multiprocessing import Pool
from os.path import splitext

from apyml import ColorStatus
from apyml.context import Context
from apyml.core.dataframe import create_dataframe_from_src
from apyml.core.preprocessing import test
from apyml.internal import *
from apyml.internal.hash import merkle_root

context = Context()

class APYML(object):
    def __init__(self, src: str, mode: str = None, report: str = None):
        self._dataframe = None
        self._infos = {}
        self._mode = 'predict' if not mode else mode
        self._src = src

        name, ext = '' , ''
        if self._src.find('s3://') > -1:
            from urllib.parse import urlparse
            infos = urlparse(self._src)
            self._infos['bucket'] = infos.netloc
            name, ext = splitext(infos.path)
            self._infos['type'] = 'S3'
        else:
            name, ext = splitext(self._src)
            self._infos['type'] = 'File'
        self._infos['extension'] = ext
        self._infos['path'] = name + ext
        self._infos['name'] = name[name.rfind('/')+1:]+ext
        info(f'Core initialization [{ColorStatus.SUCCESS}]')
    
    def run(self):
        try:
            tmp = dict(self._infos)
            path, typ, ext = tmp['path'], tmp['type'], tmp['extension']
            for k in ['path', 'type', 'extension']:
                tmp.pop(k, None)

            self._dataframe = create_dataframe_from_src(path, typ, ext, **tmp)
            info(f'Dataframe creation [{ColorStatus.SUCCESS}]')
            print(self._dataframe.describe())

            # test()
        except Exception:
            raise
    
    def report(self):
        info('APYML writing report to disk...')        

    # def _init_build(self, predict: bool = False):
    #     try:
    #         self.infos = Filepath(self._datapath).get_infos()
    #         self._dataframe = Framator(self.infos).create_dataframe()
    #         info('Dataframe creation [\033[0;32mOK\033[0m]')
    #         self._dataframe = Preprocess(self._dataframe, predict=predict)
    #         info('Data preprocessing [\033[0;32mOK\033[0m]')
    #         
    #     except Exception as e:
    #         
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