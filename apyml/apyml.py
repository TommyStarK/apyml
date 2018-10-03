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

    def _worker(self, job: dict, preprocessing_opts: dict):
        job_name = job['name']
        job_description = job['description']
        preprocess_tasks = job['preprocessing_directives']
        job_func = job[f'{self._mode}_directive']

        self._dataframe = run_preprocessing_directives(self._dataframe, self._mode, preprocess_tasks, **preprocessing_opts)
        info(f'Data preprocessing [{ColorStatus.SUCCESS}]')

        if self._mode == 'build':
            from apyml.core.build import run_build_directive
            info(f'Building model {job_name}...')
            run_build_directive(self._dataframe, job_func, job_name, job_description)
            info(f'Model {job_name} built [{ColorStatus.SUCCESS}]')
        else:
            pass
        # self._tasks.put(job)
    
    def run(self):
        try:
            tmp = dict(self._infos)
            path, typ, ext = tmp['path'], tmp['type'], tmp['extension']
            for k in ['path', 'type', 'extension']:
                tmp.pop(k, None)

            self._dataframe = create_dataframe_from_src(path, typ, ext, **tmp)
            info(f'Dataframe creation [{ColorStatus.SUCCESS}]')

            jobs = context.get_config(self._mode)[self._mode]
            preprocessing_opts = context.get_config('preprocessing_opts')
            processes = len(jobs)
  
            pool = Pool(processes=processes)
            pool.starmap(self._worker, [(job, preprocessing_opts) for job in jobs])
            pool.close()
        except Exception:
            raise
    
    def report(self):
        info('Writing report to disk...')
        self._tasks.put(None)
        for result in iter(self._tasks.get, None):
            print(result)

    # def _build(self):
    #     try:
    #         import pickle
    #         self._init_build()
    #         from apyml.core import build
    #         for directive, model in build(self._dataframe):
    #             h = context.get_from_context(f'{directive}-dataframe_hash')
    #             pickle.dump(model, open(f"{context.get_store_root()}/{directive}/{h}", 'wb'))
    #     except Exception as e:
    #         raise e

    # def _predict_routine(self, path: str, models: list):
    #     from apyml.internal import merkle_root
    #     h = merkle_root(self._dataframe.columns)
    #     print(h)
    #     if h not in models:
    #         raise RuntimeError('No model found for this kind of dataframe')
    #     target = models[models.index(h)]
    #     import pickle
    #     model = pickle.load(open(f'{path}/{target}', 'rb'))
    #     self._preds = model.predict(self._dataframe)
    #     print(self._preds)


    # def _predict(self):
    #     self.config = context.get_config('predict')

    #     try:
    #         store = context.get_store()
    #         self._init_build(predict=True)
    #         pool = Pool(processes=len(self.config['targets']))
    #         pool.starmap(self._predict_routine, [(path, models) for path, models in self._retrieve_valid_model(store)])
    #         pool.close()
    #         pool.join()
    #     except Exception as e:
    #         fatal(e)
    #         sys.exit(1)

    # def _retrieve_valid_model(self, store: dict) -> tuple:
    #     for target in self.config['targets']:
    #         for k, v in store.items():
    #             if k.find(target) > -1:
    #                 yield (k, v)