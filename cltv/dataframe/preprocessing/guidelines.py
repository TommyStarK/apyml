from pandas import DataFrame as df

from ...dataframe import preprocessor

__all__ = ['_shuffling']

@preprocessor
def _shuffling(config: dict, dataframe: df) -> df:
    print('DANS SHUFFLING')
    print(config)
    print(dataframe.shape)
    return dataframe
