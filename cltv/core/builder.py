
def build_directive(func: object):
    def wrapper():
        func()
    return wrapper
