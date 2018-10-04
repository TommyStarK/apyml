from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing import Queue
from os.path import splitext

from apyml import ColorStatus
from apyml.context import Context
from apyml.core.dataframe import create_dataframe_from_src
from apyml.core.preprocessing import run_preprocessing_directives
from apyml.internal import *

context = Context()
tasks = Manager().Queue()

class APYML(object):
    def __init__(self, src: str, mode: str = None, report: str = None, tasks: Queue = tasks):
        self._dataframe = None
        self._infos = {}
        self._mode = 'predict' if not mode else mode
        self._src = src
        self._tasks = tasks

        name, ext = '' , ''
        if self._src.find('s3://') > -1:
            from urllib.parse import urlparse
            infos = urlparse(self._src)
            self._infos['bucket'] = infos.netloc
            name, ext = splitext(infos.path)
            self._infos['type'] = 'S3'
        else:
            name, ext = splitext(self._src)
            self._infos['type'] = 'File'
        self._infos['extension'] = ext
        self._infos['path'] = name + ext
        self._infos['name'] = name[name.rfind('/')+1:]+ext
        info(f'Core initialization [{ColorStatus.SUCCESS}]')

    def _worker(self, job: dict):
        try:
            directives = job['preprocessing_directives']
            self._dataframe = run_preprocessing_directives(self._dataframe, directives)
            info(f'Data preprocessing [{ColorStatus.SUCCESS}]')
        except Exception:
            critical(f'Data preprocessing [{ColorStatus.FAILURE}]')
            raise

        if self._mode == 'build':
            from apyml.core.build import run_build_directive
            run_build_directive(self._dataframe, job)
        else:
            from apyml.core.predict import run_predict_directive
            run_predict_directive(self._dataframe, job)

        self._tasks.put({'job': job, 'timer_preprocessing': None, 'timer_job': None})
    
    def run(self):
        tmp = dict(self._infos)
        jobs = context.get_from_config(self._mode)[self._mode]
        process_number = len(jobs)
        path, typ, ext = tmp['path'], tmp['type'], tmp['extension']
        
        for k in ['path', 'type', 'extension']:
            tmp.pop(k, None)

        try:
            self._dataframe = create_dataframe_from_src(path, typ, ext, storage_infos={**tmp})
            info(f'Dataframe creation [{ColorStatus.SUCCESS}]')
        except Exception:
            fatal(f'Dataframe creation [{ColorStatus.FAILURE}]')
            raise
            return

        pool = Pool(processes=process_number)
        pool.starmap(self._worker, [(job,) for job in jobs])
        pool.close()
    
    def report(self):
        info('Writing report to disk...')
        self._tasks.put(None)
        for result in iter(self._tasks.get, None):
            print(result)