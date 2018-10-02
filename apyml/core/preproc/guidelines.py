from pandas import DataFrame as df

from ...core import preprocessor
from ...internal import info

@preprocessor
def churn_segmenting(self, dataframe: df) -> df:
    info('Churn segmenting...')
    import numpy
    def churn_to_tuple(x: float) -> tuple:
        if numpy.isnan(x):
            return (-1.0, 0.0)
        return (0.9, 1.0) if round(x, 1) == 1.0 else (round(x, 1), round(round(x, 1)+0.1, 1))
    segments = [churn_to_tuple(x) for x in [round(x*0.1, 1) for x in range (0, 11)]]
    segments.pop()
    dataframe['churn_category'] = dataframe.apply(lambda x: segments.index(churn_to_tuple(x['pchurn'])), axis=1)
    return dataframe

@preprocessor
def label_encoding(config: dict, dataframe: df) -> df:
    info('Label encoding...')
    targets = dataframe.select_dtypes(include='object')
    targets = list(targets.columns.values)
    if config['index'] in targets:
        targets.remove(config['index'])
    from sklearn.preprocessing import LabelEncoder
    encoder = LabelEncoder()
    for x in targets:
        dataframe.loc[:,(x)] = encoder.fit_transform(dataframe[x])
    return dataframe

@preprocessor
def outliers(config: dict, dataframe: df) -> df:
    import numpy
    info('Removing outliers...')
    sales = config['to_predict']
    targets = numpy.sort(numpy.array(dataframe[sales]))
    outliers = targets[:int((1 - (1/1000))*len(targets))]
    dataframe = dataframe[dataframe[sales] <= max(outliers)]
    return dataframe

@preprocessor
def set_index(config: dict, dataframe: df) -> df:
    info('Setting index...')
    dataframe = dataframe.set_index(config['index'])
    return dataframe

@preprocessor
def shuffling(config: dict, dataframe: df) -> df:
    info('Shuffling dataframe...')
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    return dataframe
