import sys
from os.path import splitext

class Filepath(object):
    def __init__(self, filepath: str):
        self.infos = {}
        self.filepath = filepath
        self._handler()

    def _handler(self):
        name, ext = '' , ''
        try:
            if self.filepath.find('s3://') > -1:
                from urllib.parse import urlparse
                infos = urlparse(self.filepath)
                self.infos['bucket'] = infos.netloc
                name, ext = splitext(infos.path)
                self.infos['type'] = 'S3'
            else:
                name, ext = splitext(self.filepath)
                self.infos['type'] = 'File'
        except Exception as e:
            raise e
        finally:
            self.infos['extension'] = ext
            self.infos['full'] = name + ext
            self.infos['name'] = name

    def get_infos(self) -> dict:
        return self.infos
