import importlib
from pandas import DataFrame as df

from apyml.context import Context

context = Context()

def run_preprocessing_directives(dataframe: df, directives: list) -> df:
    if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
        raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')

    config = context.get_from_config(['data', 'preprocessing_opts'])
    for directive in directives:
        dataframe = getattr(importlib.import_module('apyml.directives.directives'), directive['name'])(dataframe, config)
    return dataframe