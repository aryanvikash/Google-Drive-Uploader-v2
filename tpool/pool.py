import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future

from functools import wraps

_THREAD_POOL = ThreadPoolExecutor(max_workers=50)
_PROCESS_POOL = ProcessPoolExecutor()


def run_in_thread(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return asyncio.wrap_future((executor or _THREAD_POOL).submit(f, *args, **kwargs))

    return wrap


def run_in_process(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return asyncio.wrap_future((executor or _PROCESS_POOL).submit(f, *args, **kwargs))

    return wrap
