path = 'cltv.core.predict.guidelines'

def predict_routine(func: object):
    def wrapper():
        func()
    return wrapper
