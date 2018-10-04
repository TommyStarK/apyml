import pandas

class Handler(object):
    def __init__(self, readers_opts: dict, storage_infos: dict):
        self._readers_opts = readers_opts
        self._storage_infos = storage_infos

    def read_from_src(self, path: str, typ: str, extension: str) -> pandas.DataFrame:
        return {
            'File': self._fileHandler,
            'S3': self._s3Handler
        }.get(typ, None)(path, extension)

    def _fileHandler(self, path: str, extension: str) -> pandas.DataFrame:
       return getattr(self, '_read_'+extension[1:])(path)

    def _read_csv(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_csv(path_or_buff, **self._readers_opts['csv'])

    def _read_json(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_json(path_or_buff, **self._readers_opts['json'])

    def _read_parquet(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_parquet(path_or_buff, **self._readers_opts['parquet'])

    def _s3Handler(self, path: str, extension: str) -> pandas.DataFrame:
        print(path, extension)
        print(self._storage_infos)
        return None

def create_dataframe_from_src(path: str, typ: str, extension: str, storage_infos: dict = None) -> pandas.DataFrame:
    from apyml.context import Context
    context = Context()
    reader_opts = context.get_from_config('readers_opts')
    handler = Handler(reader_opts, storage_infos)
    return handler.read_from_src(path, typ, extension)