import importlib

from pandas import DataFrame as df

from ..context import Context
from ..internal import error
from ..internal import info

context = Context()

config = {
    **context.get_config('data'),
    **context.get_config('preprocessing'),
    **context.get_config('predict')
}

# path = 'apyml.core.preprocessing.guidelines'

# def preprocessor(func: object):
#     print(func)
#     def wrapper(config: dict, dataframe: df) -> df:
#         return func(config, dataframe.copy())
#     return wrapper

# def Preprocess(dataframe: df, predict: bool = False) -> df:
#     if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
#         raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')
#     tmp = dataframe.copy()
#     routines = config['routines'] if not predict else config['build_directives']
#     for routine in routines:
#         tmp = getattr(importlib.import_module(path), routine)(config, tmp)
#     return tmp


def Preprocess():
    getattr(importlib.import_module(context.get_directives()), 'test')(None, None)