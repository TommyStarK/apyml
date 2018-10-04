import os
from pandas import DataFrame as df

from apyml.context import Context
from apyml.internal import *
from apyml.internal.hash import merkle_root

context = Context()

def set_dataframe_hash_to_context(dataframe: df):
    columns = list(dataframe.columns.values)
    target = context.get_from_config('dataset')['target']

    if target in columns:
        columns.remove(target)

    dataframe_hash = merkle_root(columns)
    context.set(os.getpid(), dataframe_hash)
    return

def build_directive(func: object):
    def wrapper(dataframe: df) -> object:
        set_dataframe_hash_to_context(dataframe)
        return func(dataframe)
    return wrapper


def predict_directive(func: object):
    def wrapper(dataframe: df, path: str) -> object:
        set_dataframe_hash_to_context(dataframe)
        return func(
            dataframe, 
            context.get_available_models(
                path,
                context.get(os.getpid())
            )
        )
    return wrapper

def preprocess_directive(func: object):
    def wrapper(dataframe: df) -> df:
        return func(dataframe.copy())
    return wrapper