from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing import Queue
import os
import time

from apyml import ColorStatus
from apyml.context import Context
from apyml.core.dataframe import create_dataframe_from_src
from apyml.core.preprocessing import run_preprocessing_directives
from apyml.internal import *

tasks = Manager().Queue()

class APYML(object):
    def __init__(self, src: str, mode: str = None, report: str = None, tasks: Queue = tasks):
        self._dataframe = None
        self._infos = {}
        self._mode = 'predict' if not mode else mode
        self._preds = {}
        self._src = src
        self._tasks = tasks

        name, ext = '' , ''
        if self._src.find('s3://') > -1:
            from urllib.parse import urlparse
            infos = urlparse(self._src)
            self._infos['bucket'] = infos.netloc
            name, ext = os.path.splitext(infos.path)
            self._infos['type'] = 'S3'
        else:
            name, ext = os.path.splitext(self._src)
            self._infos['type'] = 'File'
        self._infos['extension'] = ext
        self._infos['path'] = name + ext
        self._infos['name'] = name[name.rfind('/')+1:]+ext
        info(f'Core initialization [{ColorStatus.SUCCESS}]')

    def _worker(self, job: dict):
        _id = os.getpid()
        job_duration = 0
        preprocess_duration = 0
        preprocess_start = time.time()
        directives = job['preprocessing_directives']

        self._dataframe = run_preprocessing_directives(self._dataframe, directives)
        job_start = time.time()

        if self._mode == 'build':
            from apyml.core.build import run_build_directive
            run_build_directive(self._dataframe, job)
        else:
            from apyml.core.predict import run_predict_directive
            self._preds[_id] = run_predict_directive(self._dataframe, job)
 
        now = time.time()
        self._tasks.put(
            {
                'id': _id,
                'job': job, 
                'timer_preprocessing': f'{job_start-preprocess_start}s', 
                'timer_job': f'{now-job_start}s',
                'preds': None if _id not in self._preds else self._preds[_id]
            }
        )
    
    def run(self):
        tmp = dict(self._infos)
        jobs = Context().get_from_config(self._mode)[self._mode]
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
        for item in iter(self._tasks.get, None):
            print(item)