import os
from pandas import DataFrame as df

from apyml.context import Context
from apyml.internal import *
from apyml.internal.hash import merkle_root

context = Context()

def build_directive(func: object):
    def wrapper(dataframe: df) -> object:
        columns = list(dataframe.columns.values)
        target = context.get_from_config('data')['target']
        ctx_key = f'{os.getpid()}-{target}-{dataframe.shape[0]}-{dataframe.shape[1]}'

        if target in columns:
            columns.remove(target)
        dataframe_hash = merkle_root(columns)
        context.set(ctx_key, dataframe_hash)

        return func(dataframe)
    return wrapper

def predict_directive(func: object):
    def wrapper(dataframe: df, dest: str, target: str) -> object:
        columns = list(dataframe.columns.values)
        target = context.get_from_config('data')['target']

        if target in columns:
            columns.remove(target)

        dataframe_hash = merkle_root(columns)
        models = context.get_available_models(dest, dataframe_hash)
        return func(dataframe, models)
    return wrapper

def preprocess_directive(func: object):
    def wrapper(dataframe: df, config: dict) -> df:
        return func(dataframe.copy(), config)
    return wrapper