#
# Do not remove those imports
#
import pandas


from apyml.core import build_directive
from apyml.core import predict_directive
from apyml.core import preprocess_directive
from apyml.internal import critical
from apyml.internal import debug
from apyml.internal import info
from apyml.internal import fatal
#
#
#

@preprocess_directive
def set_index(dataframe: pandas.DataFrame, config: dict) -> pandas.DataFrame:
    info('Setting index...')
    dataframe = dataframe.set_index(config['index'])
    return dataframe

@preprocess_directive
def label_encoding(dataframe: pandas.DataFrame, config: dict) -> pandas.DataFrame:
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

@preprocess_directive
def shuffling(dataframe: pandas.DataFrame, config: dict) -> pandas.DataFrame:
    info('Shuffling dataframe...')
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    return dataframe

@build_directive
def future_sales_prediction(dataframe: pandas.DataFrame) -> object:
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    future_sales = dataframe['future_sales']
    dataframe = dataframe.drop(['future_sales'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(dataframe, future_sales, test_size=0.33)
    model = xgb.XGBRegressor(nthreads=-1, booster='gbtree', objective='reg:linear', random_state=42)
    model.fit(X_train, y_train)
    return model

# @preprocessor
# def outliers(config: dict, dataframe: df) -> df:
#     import numpy
#     info('Removing outliers...')
#     sales = config['to_predict']
#     targets = numpy.sort(numpy.array(dataframe[sales]))
#     outliers = targets[:int((1 - (1/1000))*len(targets))]
#     dataframe = dataframe[dataframe[sales] <= max(outliers)]
#     return dataframe

# @preprocessor
# def churn_segmenting(self, dataframe: df) -> df:
#     info('Churn segmenting...')
#     import numpy
#     def churn_to_tuple(x: float) -> tuple:
#         if numpy.isnan(x):
#             return (-1.0, 0.0)
#         return (0.9, 1.0) if round(x, 1) == 1.0 else (round(x, 1), round(round(x, 1)+0.1, 1))
#     segments = [churn_to_tuple(x) for x in [round(x*0.1, 1) for x in range (0, 11)]]
#     segments.pop()
#     dataframe['churn_category'] = dataframe.apply(lambda x: segments.index(churn_to_tuple(x['pchurn'])), axis=1)
#     return dataframe