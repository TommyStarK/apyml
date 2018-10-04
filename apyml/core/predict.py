import pandas

from apyml.context import Context


def run_predict_directive(dataframe: pandas.DataFrame, job: dict):
    pass

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