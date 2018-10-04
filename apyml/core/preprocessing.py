import importlib
from pandas import DataFrame as df

from apyml import ColorStatus
from apyml.internal import critical, info

def run_preprocessing_directives(dataframe: df, directives: list) -> df:
    if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
        raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')

    try:
        for d in directives:
            dataframe = getattr(importlib.import_module('apyml.directives.directives'), d['name'])(dataframe)
        info(f'Data preprocessing [{ColorStatus.SUCCESS}]')
    except Exception:
        critical(f'Data preprocessing [{ColorStatus.FAILURE}]')
        raise
    return dataframe
