import logging
from functools import wraps

logger = logging.getLogger(__name__)

def logw(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            f"Calling function {func.__name__} with arguments {args} and keyword arguments {kwargs}"
        )
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} returned {result}")
        return result

    return wrapper
