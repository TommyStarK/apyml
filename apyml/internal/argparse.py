from argparse import Action

class Mode(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'mode',  self.dest)
        setattr(namespace, self.dest,  True)
