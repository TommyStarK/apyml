import logging

def init_logger():
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger('root')
    logger.addHandler(handler)
    info('Initialization logger succeeded')

def critical(message: str):
    logger = logging.getLogger('root')
    logger.setLevel(logging.CRITICAL)
    logger.critical(message)

def debug(message: str):
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)
    logger.debug(message)

def error(message: str):
    logger = logging.getLogger('root')
    logger.setLevel(logging.ERROR)
    logger.error(message)

def fatal(message: str):
    logger = logging.getLogger('root')
    logger.setLevel(logging.FATAL)
    logger.fatal(message)

def info(message: str):
    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    logger.info(message)
