from functools import wraps

from loguru import logger

logger.remove()
logger.add(
    sink = r"/Users/katarina/PycharmProjects/API/logs.log",
    level='INFO',
    format='{time} | {level} | {message}',
    rotation="10MB",
    retention="10 days"
)

def log(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Error in {func.__name__} : {str(e)}')
            raise
    return wrapper
