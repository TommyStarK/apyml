import importlib
import pickle
import os
import types

import os

import pandas

from apyml import ColorStatus
from apyml.context import Context
from apyml.internal import info, fatal
from apyml.internal.hash import merkle_root


def run_build_directive(dataframe: pandas.DataFrame, job: dict):
    name = job['name']
    func = job['build_directive']
    dest = f'{Context().get_store_path()}/{name}/{func}'
    
    try:
        info(f'Building model {name}...')
        res = getattr(importlib.import_module('apyml.directives.directives'), func)(dataframe.copy())
        dataframe_hash = Context().get(os.getpid())

        if not os.path.exists(dest):
            os.makedirs(dest)

        if isinstance(res, types.GeneratorType):
            i = 0
            for r in res:
                pickle.dump(r, open(f"{dest}/{dataframe_hash}__STEP__{chr(ord('A') + i)}", 'wb'))
                i += 1
        else:
            pickle.dump(res, open(f'{dest}/{dataframe_hash}', 'wb'))

        info(f'Model {name} built [{ColorStatus.SUCCESS}]')
    except Exception:
        fatal(f'Building model {name} [{ColorStatus.FAILURE}]')
        raise

    