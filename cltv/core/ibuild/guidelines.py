
import xgboost as xgb
from pandas import DataFrame as df

from ...core import build_directive

@build_directive
def future_sales(dataframe: df) -> object:
    from sklearn.model_selection import train_test_split
    future_sales = dataframe['future_sales']
    dataframe = dataframe.drop(['future_sales'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(dataframe, future_sales, test_size=0.33)
    model = xgb.XGBRegressor(nthreads=-1, booster='gbtree', objective='reg:linear', random_state=42)
    model.fit(X_train, y_train)
    return model
