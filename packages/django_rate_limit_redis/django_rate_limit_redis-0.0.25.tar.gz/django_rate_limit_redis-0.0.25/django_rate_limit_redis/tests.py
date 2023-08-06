from django_rate_limit_redis.decorators import rate_limit
from django_rate_limit_redis.models import RateLimit
import redis

from django.conf import settings
from django.test import TestCase


class RedisRateLimiterTestCase(TestCase):
    """
    Check the limiter of requests to set a lock, save the cache,
    prevent repeated calls when a lock is set.
    The work of the decorator is also checked.
    """

    def setUp(self):
        self.test_methods_1 = ["СБИС.Тест", "/V3/GetDocuments"]
        self.test_methods_2 = ["СБИС.Тест_2", "/V3/GetDocuments/2"]
        self.test_methods_3 = ["СБИС.Тест_3", "/V3/GetDocuments/3"]
        self.test_methods_4 = ["СБИС.Тест_4", "/V3/GetDocuments/4"]
        self.system = "some_system"
        self.connection = redis.from_url(settings.RATELIMITER_REDIS_URL)
        self.connection.flushall()
        super().setUp()

    def rate_limit_decorator_test(self, system, test_method):
        @rate_limit(
            system=system,
            limit=1,
            window=10,
            blocking_timeout=1,
        )
        def limit_test(method_name: str):
            return method_name

        return limit_test(method_name=test_method)

    def test_decorator_and_lock(self):
        for test_method in self.test_methods_1:
            method_name = self.rate_limit_decorator_test(self.system, test_method)
            self.assertEqual(test_method, method_name)
            self.assertTrue(
                bool(self.connection.exists(f"RateLimiter.request.{test_method}.lock"))
            )

    def test_rate_limit_cache(self):
        for test_method in self.test_methods_2:
            method_name = self.rate_limit_decorator_test(self.system, test_method)
            self.assertTrue(bool(self.connection.get(method_name)))

    def test_rate_limit_orm_data(self):
        for test_method in self.test_methods_3:
            method_name = self.rate_limit_decorator_test(self.system, test_method)
            obj = RateLimit.objects.get(api_method=test_method, system=self.system,)
            timeout = round(obj.window / obj.limit, 3)
            self.assertEqual(float(self.connection.get(method_name)), timeout)

    def test_rate_limit_lock(self):
        for test_method in self.test_methods_4:
            method_name = self.rate_limit_decorator_test(self.system, test_method)
            try_method_name = self.rate_limit_decorator_test(self.system, test_method)
            self.assertEqual(test_method, method_name)
            self.assertNotEqual(try_method_name, method_name)
