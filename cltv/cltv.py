import sys

from multiprocessing import Pool

from .core import Framator
from .core import Preprocess
from .context import Context
from .internal import Filepath
from .internal import merkle_root
from .internal import fatal
from .internal import info

context = Context()

class CLTV(object):
    def __init__(self, datapath: str, mode: str = None):
        self._dataframe = None
        self._datapath = datapath
        self._handler = { 'build': self._build, 'predict': self._predict }
        if not mode:
            self._mode = 'predict'
        else:
            self._mode = mode

    def _init_build(self, predict: bool = False):
        try:
            self.infos = Filepath(self._datapath).get_infos()
            self._dataframe = Framator(self.infos).create_dataframe()
            info('Dataframe creation [\033[0;32mOK\033[0m]')
            self._dataframe = Preprocess(self._dataframe, predict=predict)
            info('Data preprocessing [\033[0;32mOK\033[0m]')
            info('CLTV initialization [\033[0;32mOK\033[0m]')
        except Exception as e:
            fatal('CLTV initialization [\033[0;31mFAILED\033[0m]')
            fatal(e)
            sys.exit(1)


    def _build(self):
        try:
            import pickle
            self._init_build()
            from .core import build
            for directive, model in build(self._dataframe):
                h = context.get_from_context(f'{directive}-dataframe_hash')
                pickle.dump(model, open(f"{context.get_store_root()}/{directive}/{h}", 'wb'))
        except Exception as e:
            raise e

    def _predict_routine(self, path: str, models: list):
        from .internal import merkle_root
        h = merkle_root(self._dataframe.columns)
        print(h)
        if h not in models:
            raise RuntimeError('No model found for this kind of dataframe')
        target = models[models.index(h)]
        import pickle
        model = pickle.load(open(f'{path}/{target}', 'rb'))
        preds = model.predict(self._dataframe)
        # Manouchage en vu de la demo
        import pandas
        spreds = pandas.Series(preds)
        res = pandas.read_csv('~/Downloads/itm_sales_measured.csv')
        print(res.head())
        from sklearn.metrics import mean_squared_error
        print(f"MSE -> {mean_squared_error(res['future_sales'], preds)}")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.scatter(res['future_sales'], spreds, edgecolors=(0, 0, 0))
        ax.plot([res['future_sales'].min(), res['future_sales'].max()], [res['future_sales'].min(), res['future_sales'].max()], 'k--', lw=4)
        ax.set_xlabel('Measured')
        ax.set_ylabel('Predicted')
        plt.show()



    def _predict(self):
        self.config = context.get_config('predict')

        try:
            store = context.get_store()
            self._init_build(predict=True)
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
        self._handler[self._mode]()
