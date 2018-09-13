import sys
import pandas

from ..context import Context
from ..connector import S3Conn
from ..internal import error
from ..internal import info

class Framator(object):
    def __init__(self, infos: dict):
        context = Context()
        self.infos = infos
        if not self.infos:
            raise RuntimeError('Framator init empty dict')
        self.config = context.get_config('loaders')

    def _filehandler(self) -> pandas.DataFrame:
       return getattr(self, '_read_'+self.infos['extension'][1:])(self.infos['full'])

    def _read_csv(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_csv(path_or_buff, **self.config['csv'])

    def _read_json(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_json(path_or_buff, **self.config['json'])

    def _read_parquet(self, path_or_buff: object) -> pandas.DataFrame:
        return pandas.read_parquet(path_or_buff, **self.config['parquet'])

    def _s3handler(self) -> pandas.DataFrame:
        return None

    def create_dataframe(self) -> pandas.DataFrame:
        info('Creating new dataframe...')
        return {
            'File': self._filehandler,
            'S3': self._s3handler
        }.get(self.infos['type'], None)()
