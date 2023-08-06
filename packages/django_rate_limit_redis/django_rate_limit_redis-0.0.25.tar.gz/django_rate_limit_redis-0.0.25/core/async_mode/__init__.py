import multiprocessing
from multiprocessing import cpu_count
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from django.core.cache import cache
from django.db import close_old_connections
from django.db import connection

from core.conf import Settings


class AsyncResult:
    def __init__(self, func, process):
        self.func = func
        self.process = process

    def async_result(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        if self.process:
            return result
        connection.close()
        close_old_connections()
        return result


class AsyncBase:

    def __init__(self, pool_size=None, upscale=2, use_process=False):
        self._use_process = use_process
        if use_process:
            '''Not using for ORM!!!'''
            pool = Pool
        else:
            pool = ThreadPool

        if pool_size:
            self._pool_size = pool_size
        else:
            self._upscale = upscale
            self._pool_size = cpu_count() * upscale

        self._pool = pool(processes=self._pool_size)
        self.inputs = []
        self.results = []
        self.errors = []
        self._apply_async_list = []

    def _update_result(self, result):
        if isinstance(self.results, list):
            self.results.append(result)

    def _update_errors(self, ex):
        print(ex)

    def clear_attr(self):
        self.inputs = []
        self.results = []
        self.errors = []
        self._apply_async_list = []

    def refresh_pool(self):
        self._pool.close()
        self._pool.terminate()
        self._pool = multiprocessing.Pool(processes=self._pool_size)

    def apply_async(self, func, *args, **kwargs):
        apply_result = self._pool.apply_async(
            AsyncResult(func, self._use_process).async_result, args=args, kwds=kwargs,
            callback=self._update_result,
            error_callback=self._update_errors
        )
        self._apply_async_list.append(apply_result)
        return apply_result

    def map(self, func, inputs):
        self._apply_async_list = []
        self.results = self._pool.map(AsyncResult(func, self._use_process).async_result, inputs)
        return self.results

    def get(self):
        if self._apply_async_list:
            for item in self._apply_async_list:
                item.wait()
        self._apply_async_list = []
        return self.results

    def __del__(self):
        self._pool.close()
        self._pool.terminate()


class AsyncPool(AsyncBase):
    def __init__(self, pool_size=None, upscale=2, use_process=False):
        self.conf = Settings()
        if pool_size:
            self.pool_size = pool_size
        else:
            self.upscale = upscale
            self.pool_size = cpu_count() * upscale

        self._free_process = self._free_processes()
        self.pool_size = self._pool_size(self._free_process, self.pool_size)
        self._async_mode = self._chek_async_mode(self.pool_size)
        if self._async_mode:
            super().__init__(pool_size=self.pool_size, upscale=upscale, use_process=use_process)
            cache.set('async_process_count', cache.get('async_process_count', 0) + self.pool_size)
        self.inputs = []
        self.results = []
        self.errors = []
        self._apply_async_list = []

    def __del__(self):
        if self._async_mode:
            super().__del__()
            async_process_sum = cache.get('async_process_count', 0) - self.pool_size
            if async_process_sum < 0:
                async_process_sum = 0
            cache.set('async_process_count', async_process_sum)

    def _free_processes(self):
        async_process_count = cache.get('async_process_count', 0)
        limit_async_process = self.conf.ASYNC_PROCESS_COUNT_LIMIT
        free_processes = 0
        if async_process_count and async_process_count >= 0:
            free_processes = limit_async_process - async_process_count
            return free_processes
        elif async_process_count < 0:
            return free_processes
        return limit_async_process

    def _pool_size(self, free_process, pool_size):
        if pool_size <= free_process:
            return pool_size
        elif pool_size > free_process:
            return free_process

    def _chek_async_mode(self, pool_size):
        if pool_size > 0:
            return True
        return False

    def refresh_pool(self):
        if self._async_mode:
            super().refresh_pool()

    def apply_async(self, func, *args, **kwargs):
        if self._async_mode:
            return super().apply_async(func, *args, **kwargs)
        result = func(*args, **kwargs)
        self.results.append(result)
        return result

    def map(self, func, inputs):
        if self._async_mode:
            return super().map(func, inputs)
        self.results = map(func, inputs)
        return self.results

    def get(self):
        if self._async_mode:
            return super().get()
        return self.results
