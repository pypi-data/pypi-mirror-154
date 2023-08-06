from datetime import datetime
from datetime import timedelta
import time

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase

from core.async_mode import AsyncPool


class TestMethods:

    def args_kwargs_test(self, some_arg, some_kwarg=None):
        if some_kwarg:
            return some_arg, {'some_kwarg': some_kwarg}
        return some_arg

    def async_run_sleep_test(self, *args, **kwargs):
        time.sleep(1)

    def write_users(self, user_name):
        Users = get_user_model()
        user_pk = Users.objects.create(username=user_name).pk
        return user_pk

    def read_users(self, user_name):
        Users = get_user_model()
        user_pk = Users.objects.get(username=user_name).pk
        return user_pk


class BaseTestCase:
    pool_size = 8
    async_pool = None
    reference_time = timedelta(seconds=2.03)

    def args_kwargs_test(self, some_arg, some_kwarg=None):
        if some_kwarg:
            return some_arg, {'some_kwarg': some_kwarg}
        return some_arg

    def apply_async_args_kwargs(self):
        self.async_pool.clear_attr()
        some_arg = [x for x in range(0, 10)]
        some_kwarg = 'some_kwarg'
        result = some_arg, {'some_kwarg': some_kwarg}
        self.async_pool.apply_async(self.test_methods.args_kwargs_test, some_arg, some_kwarg=some_kwarg)
        self.assertEqual([result], list(self.async_pool.get()))

    def map_args(self):
        self.async_pool.clear_attr()
        inputs = [f'item_{x}' for x in range(0, 10)]
        self.async_pool.map(self.test_methods.args_kwargs_test, inputs)
        self.assertEqual(inputs, list(self.async_pool.get()))

    def apply_async_time(self):
        self.async_pool.clear_attr()
        some_arg = [x for x in range(0, 10)]
        start_time = datetime.now()
        self.async_pool.apply_async(self.test_methods.async_run_sleep_test, some_arg)
        self.async_pool.get()
        verif_time = datetime.now() - start_time
        self.assertGreaterEqual(self.reference_time, verif_time)

    def map_time(self):
        self.async_pool.clear_attr()
        inputs = [f'item_{x}' for x in range(0, 10)]
        start_time = datetime.now()
        self.async_pool.map(self.test_methods.async_run_sleep_test, inputs)
        verif_time = datetime.now() - start_time
        self.assertGreaterEqual(self.reference_time, verif_time)

    def cache_get_set(self):
        cache_pool_size = cache.get('async_process_count')
        self.assertEqual(cache_pool_size, self.pool_size)
        self.async_pool.__del__()
        cache_pool_size_after_del = cache_pool_size - self.pool_size
        self.assertEqual(cache.get('async_process_count'), cache_pool_size_after_del)

    def orm_rw_map(self):
        self.async_pool.clear_attr()
        user = 'Test_user'
        inputs_list_users = [f'{user}_{x}' for x in range(0, 9)]
        list_write_orm_users = self.async_pool.map(self.test_methods.write_users, inputs_list_users)
        list_read_orm_users = self.async_pool.map(self.test_methods.read_users, inputs_list_users)
        self.assertEqual(list(list_write_orm_users), list(list_read_orm_users))


class AsyncPoolThreadTestCase(TestCase, BaseTestCase):
    fixtures = ("Settings",)

    def setUp(self):
        self.async_pool = AsyncPool(pool_size=self.pool_size)
        self.test_methods = TestMethods()

    def test_apply_async_args_kwargs(self):
        super().apply_async_args_kwargs()

    def test_map_args_kwargs(self):
        super().map_args()

    def test_apply_async_time(self):
        super().apply_async_time()

    def test_map_time(self):
        super().map_time()

    def test_get_set_cache(self):
        super().cache_get_set()

    def test_orm_rw_map(self):
        super().orm_rw_map()


class AsyncPoolProcessTestCase(TestCase, BaseTestCase):
    fixtures = ("Settings",)

    def setUp(self):
        self.async_pool = AsyncPool(pool_size=8, use_process=True)
        self.test_methods = TestMethods()

    def test_apply_async_args_kwargs(self):
        super().apply_async_args_kwargs()

    def test_map_args_kwargs(self):
        super().map_args()

    def test_apply_async_time(self):
        super().apply_async_time()

    def test_map_time(self):
        super().map_time()

    def test_get_set_cache(self):
        super().cache_get_set()

    # def test_orm_rw_map(self):
    #     '''No using fo ORM!!!'''
    #     super().orm_rw_map()
