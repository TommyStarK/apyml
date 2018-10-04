import importlib
import pickle
import os
import types

import pandas

from apyml import ColorStatus
from apyml.context import Context
from apyml.internal import info
from apyml.internal.hash import merkle_root


def run_build_directive(dataframe: pandas.DataFrame, job: dict):
    build_name = job['name']
    build_description = job['description']
    build_func = job['build_directive']

    context = Context()
    target = context.get_from_config('data')['target']
    ctx_key = f'{os.getpid()}-{target}-{dataframe.shape[0]}-{dataframe.shape[1]}'
    dest = f'{context.get_store_path()}/{build_name}/{build_func}'

    info(f'Building model {build_name}...')
    res = getattr(importlib.import_module('apyml.directives.directives'), build_func)(dataframe.copy())
    dataframe_hash = context.get(ctx_key)

    if not os.path.exists(dest):
        os.makedirs(dest)

    if isinstance(res, types.GeneratorType):
        i = 0
        for r in res:
            pickle.dump(r, open(f'{dest}/{dataframe_hash}__STEP__{i}', 'wb'))
            i += 1
    else:
        pickle.dump(res, open(f'{dest}/{dataframe_hash}', 'wb'))
    info(f'Model {build_name} built [{ColorStatus.SUCCESS}]')

    