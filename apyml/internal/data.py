import sys
from os.path import splitext


class DataHandler(object):
    def __init__(self, path: str):
        self._infos = {}
        self._path = path
        
        try:
            name, ext = '' , ''
            if self._path.find('s3://') > -1:
                from urllib.parse import urlparse
                infos = urlparse(self._path)
                self._infos['bucket'] = infos.netloc
                name, ext = splitext(infos.path)
                self._infos['type'] = 'S3'
            else:
                name, ext = splitext(self._path)
                self._infos['type'] = 'File'
        except Exception as e:
            raise
        finally:
            self._infos['extension'] = ext
            self._infos['full'] = name + ext
            self._infos['name'] = name

    def get_infos(self) -> dict:
        return self._infos