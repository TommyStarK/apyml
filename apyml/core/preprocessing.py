import importlib
from pandas import DataFrame as df

from apyml.context import Context

context = Context()

def run_preprocessing_directives(dataframe: df, mode:str, directives: list, **optional_args) -> df:
    if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
        raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')

    print(mode)
    print(directives)
    print(optional_args)
    conf = context.get_config('data')
    print(conf)

    tmp = dataframe.copy()
    for directive in directives:
        tmp = getattr(importlib.import_module('apyml.directives.directives'), directive['name'])(tmp, conf)
    return tmp