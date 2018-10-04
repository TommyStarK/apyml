import pandas

from apyml.context import Context
import importlib
import types

import pandas

from apyml import ColorStatus
from apyml.context import Context
from apyml.internal import info, fatal

def run_predict_directive(dataframe: pandas.DataFrame, job: dict):
    build_name = job['name']
    model_name = job['model_name']
    predict_func = job['predict_directive']

    context = Context()
    target = context.get_from_config('data')['target']
    dest = f'{context.get_store_path()}/{build_name}/{model_name}'

    info(f'Running predictive model(s)...')
    res = getattr(importlib.import_module('apyml.directives.directives'), predict_func)(dataframe, dest, target)

    from sklearn.metrics import mean_squared_error
    import matplotlib.pyplot as plt

    def process_preds(true, preds):
        print(f"MSE -> {mean_squared_error(true, preds)}")
        fig, ax = plt.subplots()
        ax.scatter(true, preds, edgecolors=(0, 0, 0))
        ax.plot([true.min(), true.max()], [true.min(), true.max()], 'k--', lw=4)
        ax.set_xlabel('Measured')
        ax.set_ylabel('Predicted')
        plt.show()

    if isinstance(res, types.GeneratorType):
        for r in res:
            process_preds(r[0], r[1])
        return
    process_preds(res[0], res[1])