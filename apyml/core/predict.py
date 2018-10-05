import importlib
import types

import pandas

from apyml import ColorStatus
from apyml.context import Context
from apyml.internal import info, fatal

def run_predict_directive(dataframe: pandas.DataFrame, job: dict) -> pandas.DataFrame:
    func = job['predict_directive']
    model = job['model_name']
    name = job['name']
    path = f'{Context().get_store_path()}/{name}/{model}'

    final = pandas.DataFrame(
            index=[Context().get_from_config('dataset')['index']], 
            columns=[Context().get_from_config('dataset')['target'], 'predictions']
        )

    try:
        info(f'Running model(s)...')
        ret = getattr(importlib.import_module('apyml.directives.directives'), func)(dataframe, path)

        def predictions_to_dataframe(true: pandas.Series, preds) -> pandas.DataFrame:
            df = true.to_frame()
            df['predictions'] = preds
            return df.copy()

        if isinstance(ret, types.GeneratorType):
            for r in ret:
                final = pandas.concat([final, predictions_to_dataframe(r[0], r[1])])
        else:
            final = pandas.concat([final, predictions_to_dataframe(ret[0], ret[1])])
    
    except Exception:
        fatal(f'Running model(s)... [{ColorStatus.FAILURE}]')
        raise

    return final.copy()