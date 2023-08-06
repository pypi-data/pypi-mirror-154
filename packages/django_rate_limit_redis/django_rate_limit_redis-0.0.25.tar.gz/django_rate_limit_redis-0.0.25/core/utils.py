from datetime import datetime
from functools import wraps
from itertools import zip_longest
import logging
from multiprocessing import Process

from django.utils import timezone

from core.conf import Settings

logger = logging.getLogger(__name__)


def grouper(iterable, n):
    """
    grouper('ABCDEFG', 3) --> (A, B, C), (D, E, F),  (G, )
    False elements (0, False, None)  will be screened
    """
    args = [iter(iterable)] * n
    for group in zip_longest(fillvalue=None, *args):
        yield filter(None, group)


def parse_datetime(dtime):
    if not dtime:
        return None
    if dtime == '01.01.0001 0:00:00':    # 1C может прислать пустую дату в виде такого значения
        dtime = '02.01.0001 0:00:00'
    if len(dtime) > 10:
        return timezone.localtime(datetime.strptime(dtime, "%d.%m.%Y %H:%M:%S").astimezone())
    else:
        return timezone.localtime(datetime.strptime(dtime, "%Y-%m-%d").astimezone())


def lead_time(*args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            runtime = datetime.now() - start_time
            logger.log(f'func {func.__name__} runtime: {runtime}')
            if result:
                return result

        return wrapper

    return decorator


def async_process_no_return(*args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conf = Settings()
            if conf.USE_ASYNC:
                p = Process(target=func, args=args, kwargs=kwargs)
                p.start()
            else:
                func(*args, **kwargs)

        return wrapper

    return decorator
