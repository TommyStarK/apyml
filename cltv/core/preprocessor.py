import importlib

from pandas import DataFrame as df

from ..context import Context
from ..internal import error
from ..internal import info

context = Context()

config = {
    **context.get_config('data'),
    **context.get_config('preprocessing')
}

path = 'cltv.core.preprocessing.guidelines'

def preprocessor(func):
    def wrapper(config: dict, dataframe: df) -> df:
        return func(config, dataframe.copy())
    return wrapper

def Preprocess(dataframe: df) -> df:
    if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
        raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')
    tmp = dataframe.copy()
    for routine in config['routines']:
        tmp = getattr(importlib.import_module(path), routine)(config, tmp)
    return tmp
