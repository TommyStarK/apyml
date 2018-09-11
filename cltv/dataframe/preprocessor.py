from pandas import DataFrame as df

from ..context import Context
from ..internal import error
from ..internal import info

class Preprocessor(object):
    def __init__(self, dataframe: df):
        if dataframe is None or not isinstance(dataframe, df) or dataframe.empty:
            raise RuntimeError('Unprocessable dataframe. None, not of type pandas.DataFrame or empty dataframe')

        self.dataframe = dataframe.copy()

        context = Context()
        self.config = {
            **context.get_config('data'),
            **context.get_config('preprocessing')
        }

    def _churn_segmenting(self, dataframe: df) -> df:
        import math
        def churn_to_tuple(x: float) -> tuple:
            return (0.9, 1.0) if round(x, 1) == 1.0 or math.isnan(x) else (round(x, 1), round(round(x, 1)+0.1, 1))

        tmp = dataframe.copy()
        churns = [round(x*0.1, 1) for x in range (0, 11)]
        segments = [churn_to_tuple(x) for x in churns]
        segments.pop()
        tmp['churn_category'] = tmp.apply(lambda x: segments.index(churn_to_tuple(x['pchurn'])), axis=1)
        # find a way to handle NaN
        return tmp

    def _outliers(self, dataframe: df) -> df:
        import numpy
        info('Removing outliers...')
        tmp = dataframe.copy()
        sales = self.config['to_predict']
        targets = numpy.sort(numpy.array(tmp[sales]))
        outliers = targets[:int((1 - (1/1000))*len(targets))]
        tmp = tmp[tmp[sales] <= max(outliers)]
        return tmp

    def _label_encoding(self, dataframe: df) -> df:
        info('Label encoding...')
        tmp = dataframe.copy()
        targets = tmp.select_dtypes(include='object')
        targets = list(targets.columns.values)
        if self.config['index'] in targets:
            targets.remove(self.config['index'])
        from sklearn.preprocessing import LabelEncoder
        encoder = LabelEncoder()
        for x in targets:
            tmp.loc[:,(x)] = encoder.fit_transform(tmp[x])
        return tmp

    def _filling_nan(self, dataframe: df) -> df:
        return None

    def _cohort(self, dataframe: df) -> df:
        return None

    def _shuffling(self, dataframe: df) -> df:
        info('Shuffling dataframe...')
        tmp = dataframe.copy()
        tmp = tmp.sample(frac=1).reset_index(drop=True)
        return tmp

    def _set_index(self, dataframe: df) -> df:
        info('Setting index...')
        tmp = dataframe.copy()
        tmp.set_index(self.config['index'])
        return tmp

    def preprocess(self) -> df:
        info(f'Preprocessing dataframe...')
        tmp = self.dataframe.copy()
        for routine in self.config['routines']:
            tmp = getattr(self, '_'+routine)(tmp)
        return tmp
