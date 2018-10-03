import pandas

class Handler(object):
    def __init__(self, readers_opts: dict):
        self._readers_opts = readers_opts

    def read_from_src(self, path: str, typ: str, extension: str, **optional_args) -> pandas.DataFrame:
        return {
            'File': self._fileHandler,
            'S3': self._s3Handler
        }.get(typ, None)(path, extension, **optional_args)

    def _fileHandler(self, path: str, extension: str, **optional_args) -> pandas.DataFrame:
       return getattr(self, '_read_'+extension[1:])(path)

    def _read_csv(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_csv(path_or_buff, **self._readers_opts['csv'])

    def _read_json(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_json(path_or_buff, **self._readers_opts['json'])

    def _read_parquet(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_parquet(path_or_buff, **self._readers_opts['parquet'])

    def _s3Handler(self, path: str, extension: str, **optional_args) -> pandas.DataFrame:
        return None

def create_dataframe_from_src(path: str, typ: str, extension: str, **optional_args) -> pandas.DataFrame:
    from apyml.context import Context
    context = Context()

    readers_opts = context.get_from_config('readers_opts')
    handler = Handler(readers_opts)
    return handler.read_from_src(path, typ, extension, **optional_args)