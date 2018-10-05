#
# Do not remove imports below
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
# Do not remove imports above
#

#
# PREPROCESSING
#
@preprocess_directive
def label_encoding(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    info('Label encoding...')
    targets = dataframe.select_dtypes(include='object')
    targets = list(targets.columns.values)
    if 'ivname' in targets:
        targets.remove('ivname')
    for target in targets:
        dataframe[target] = dataframe[target].astype('category')
        dataframe[target] = dataframe[target].cat.codes
    return dataframe


@preprocess_directive
def outliers(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    import numpy
    info('Removing outliers...')
    targets = numpy.sort(numpy.array(dataframe['future_sales']))
    outliers = targets[:int((1 - (1/1000))*len(targets))]
    dataframe = dataframe[dataframe['future_sales'] <= max(outliers)]
    return dataframe


@preprocess_directive
def reindex(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    import numpy
    info('Reindexing dataframe...')
    dataframe = dataframe.reindex(numpy.random.RandomState(seed=42).permutation(dataframe.index))
    return dataframe


@preprocess_directive
def remove_undesired_columns(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    import numpy
    info('Removing undesired columns...')
    dataframe = dataframe.drop(['first_trans_date', 'last_trans_date', 'Unnamed: 0'], axis=1)
    return dataframe


@preprocess_directive
def set_index(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    info('Setting index...')
    dataframe = dataframe.set_index('ivname')
    return dataframe


@preprocess_directive
def shuffling(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    info('Shuffling dataframe...')
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    return dataframe


#
# BUILD
# 
@build_directive
def future_sales_by_cohort(dataframe: pandas.DataFrame) -> object:
    import numpy
    import xgboost as xgb
    
    dfs = []
    cohorts = numpy.sort(numpy.array(dataframe.cohort.unique())).tolist()
    cohorts.pop()
    i = len(cohorts) - 1
    while i - 1 >= 0:
        dfs.append(dataframe[(dataframe['cohort'] <= cohorts[i]) & (dataframe['cohort'] > cohorts[i-1])].copy())
        i -= 1
    dfs.append(dataframe[dataframe['cohort'] <= -14.0].copy())
    dfs.append(dataframe[dataframe['cohort'].isnull()].copy())

    for df in dfs:
        future_sales = df['future_sales']
        df = df.drop(['future_sales'], axis=1)
        model = xgb.XGBRegressor(nthreads=-1, booster='gbtree', objective='reg:linear', random_state=42)
        model.fit(df, future_sales)
        yield model


# 
# PREDICT
#
@predict_directive
def predict_future_sales_by_cohort(dataframe: pandas.DataFrame, models: list) -> object:
    import numpy
    
    dfs = []
    cohorts = numpy.sort(numpy.array(dataframe.cohort.unique())).tolist()
    cohorts.pop()
    i = len(cohorts) - 1
    while i - 1 >= 0:
        dfs.append(dataframe[(dataframe['cohort'] <= cohorts[i]) & (dataframe['cohort'] > cohorts[i-1])].copy())
        i -= 1
    dfs.append(dataframe[dataframe['cohort'] <= -14.0].copy())
    dfs.append(dataframe[dataframe['cohort'].isnull()].copy())

    for index, df in enumerate(dfs):
        future_sales = df['future_sales']
        df = df.drop(['future_sales'], axis=1)
        preds = models[index].predict(df)
        yield (future_sales, preds)