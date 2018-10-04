import importlib
import types

import pandas

from apyml import ColorStatus
from apyml.context import Context
from apyml.internal import info, fatal

def run_predict_directive(dataframe: pandas.DataFrame, job: dict):
    context = Context()
    build_name = job['name']
    model_name = job['model_name']
    predict_func = job['predict_directive']
    path = f'{context.get_store_path()}/{build_name}/{model_name}'

    try:
        info(f'Running model(s)...')
        ret = getattr(
            importlib.import_module('apyml.directives.directives'), 
            predict_func
        )(dataframe, path)

        def predictions_to_dataframe(true: pandas.Series, preds) -> pandas.DataFrame:
            df = true.to_frame()
            df['predictions'] = preds
            return df.copy()

        final = pandas.DataFrame(
            index=[context.get_from_config('dataset')['index']], 
            columns=[context.get_from_config('dataset')['target'], 'predictions']
        )
        print("1111", final.head(20))

        if isinstance(ret, types.GeneratorType):
            for r in ret:
                tmp = predictions_to_dataframe(r[0], r[1])
                print("22222", tmp.head(20))
                final.append(tmp, ignore_index=True)
                print("33333", final.head(20))
        else:
            tmp = predictions_to_dataframe(ret[0], ret[1])
            print("22222", tmp.head(20))
            final.append(tmp, ignore_index=True)
            print("33333", final.head(20))

        context.set(build_name, final.copy())
    except Exception:
        fatal(f'Running model(s)... [{ColorStatus.FAILURE}]')
        raise