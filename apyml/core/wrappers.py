from pandas import DataFrame as df

from apyml.context import Context
from apyml.internal import *
from apyml.internal.hash import merkle_root

def build_directive(func: object):
    def wrapper(dataframe: df) -> object:
        config = context.get_config('data')
        if 'to_predict' not in config:
            raise KeyError('Missing key `to_predict` in config.')
        targets = list(dataframe.columns.values)
        if config['to_predict'] in targets:
            targets.remove(config['to_predict'])
        context.set_to_context(f"{config['to_predict']}-dataframe_hash", merkle_root(targets))
        # info('Building model...')
        return func(dataframe)
    return wrapper

def predict_directive(func: object):
    def wrapper():
        func()
    return wrapper

def preprocess_directive(func: object):
    def wrapper(dataframe: df, config: dict) -> df:
        return func(dataframe.copy(), config)
    return wrapper