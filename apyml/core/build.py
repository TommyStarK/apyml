import os
import pickle
import importlib

import pandas

from apyml.context import Context
from apyml.internal.hash import merkle_root


def run_build_directive(dataframe: pandas.DataFrame, func: str, name: str, description: str):
    context = Context()
    to_predict = context.get_from_config('data')['to_predict']
    model = getattr(importlib.import_module('apyml.directives.directives'), func)(dataframe.copy())
    dataframe_hash = context.get(f'{to_predict}-dataframe_hash')

    if not os.path.exists(f'{context.get_store_path()}/{func}/{name}'):
        os.makedirs(f'{context.get_store_path()}/{func}/{name}')

    pickle.dump(model, open(f'{context.get_store_path()}/{func}/{name}/{dataframe_hash}', 'wb'))

    