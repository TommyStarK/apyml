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
        dataframe.loc[:,(x)] = encoder.fit_transform(dataframe[x].astype(str))
    return dataframe

@preprocess_directive
def shuffling(dataframe: pandas.DataFrame, config: dict) -> pandas.DataFrame:
    info('Shuffling dataframe...')
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    return dataframe

@preprocess_directive
def outliers(dataframe: pandas.DataFrame, config: dict) -> pandas.DataFrame:
    import numpy
    info('Removing outliers...')
    sales = config['target']
    targets = numpy.sort(numpy.array(dataframe[sales]))
    outliers = targets[:int((1 - (3/1000))*len(targets))]
    dataframe = dataframe[dataframe[sales] <= max(outliers)]
    return dataframe


@preprocess_directive
def remove_undesired(dataframe: pandas.DataFrame, config: dict) -> pandas.DataFrame:
    import numpy
    info('Removing undesired...')
    dataframe = dataframe.drop(['first_trans_date', 'last_trans_date', 'rfm_cluster_fixed_retention', 'rfm_cluster_type_fixed_retention', 'rfm_cluster_full', 'rfm_cluster_type_full'], axis=1)
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


@build_directive
def future_sales_by_cohort(dataframe: pandas.DataFrame) -> object:
    import numpy
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    
    dfs = []
    cohorts = numpy.sort(numpy.array(dataframe.cohort.unique())).tolist()
    cohorts.pop()
    i = len(cohorts) - 1
    while i - 1 >= 0:
        dfs.append(dataframe[(dataframe['cohort'] <= cohorts[i]) & (dataframe['cohort'] > cohorts[i-1])].copy())
        i -= 1
    dfs.append(dataframe[dataframe['cohort'] <= -14.0].copy())
    dfs.append(dataframe[numpy.isnan(dataframe['cohort'])].copy())

    for df in dfs:
        future_sales = df['future_sales']
        df = df.drop(['future_sales'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(df, future_sales, test_size=0.33)
        model = xgb.XGBRegressor(nthreads=-1, booster='gbtree', objective='reg:linear', random_state=42)
        model.fit(X_train, y_train)
        yield model

    
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
    dfs.append(dataframe[numpy.isnan(dataframe['cohort'])].copy())

    for index, df in enumerate(dfs):
        future_sales = df['future_sales']
        df = df.drop(['future_sales'], axis=1)
        preds = models[index].predict(df)
        yield (future_sales, preds)