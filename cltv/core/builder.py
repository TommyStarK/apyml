import importlib

from pandas import DataFrame as df

from ..context import Context
from ..internal import info
from ..internal import merkle_root

context = Context()

path = 'cltv.core.build.guidelines'

def build_directive(func: object):
    def wrapper(dataframe: df) -> object:
        config = context.get_config('data')
        if 'to_predict' not in config:
            raise KeyError('Missing key `to_predict` in config.')
        targets = list(dataframe.columns.values)
        if config['to_predict'] in targets:
            targets.remove(config['to_predict'])
        context.set_to_context(f"{config['to_predict']}-dataframe_hash", merkle_root(targets))
        info('Building model...')
        return func(dataframe)
    return wrapper


def build(dataframe: df) -> object:
    if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
        raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')

    config = context.get_config('build')
    for directive in config['targets']:
        yield (directive, getattr(importlib.import_module(path), directive)(dataframe.copy()))
