import datetime
from typing import Optional

import redis
from redis.lock import Lock
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

RATELIMITER_REDIS_URL = settings.RATELIMITER_REDIS_URL


class RedisRateLimiter(object):
    connection = None

    def __init__(
        self,
        key: str,
        limit: Optional[int] = 1,
        window: Optional[int] = 1,
        system: Optional[str] = None,
        latency: Optional[datetime.timedelta] = None,
        redis_client: Optional[redis.Redis] = None,
        redis_url: Optional[str] = None,
        blocking_timeout: Optional[int] = None,
        user=None,
    ):

        RedisRateLimiter.connection = (
            redis_client
            or RedisRateLimiter.connection
            or redis.from_url(redis_url or RATELIMITER_REDIS_URL)
        )
        self.key = key
        self.limit = limit
        self.window = window
        self.system = system
        self.latency = latency if latency else 0
        self.blocking_timeout = blocking_timeout

        from django_rate_limit_redis.models import RateLimit

        self.RateLimit = RateLimit
        if isinstance(user, AnonymousUser):
            user = None
        self.user = user

    def redis_rate_limit(self, func, *args, **kwargs):
        lock = Lock(
            redis=self.connection,
            name=f"RateLimiter.request.{self.key}.lock",
            timeout=self.get_cache_timeout(),
        )
        if lock.acquire(blocking_timeout=self.blocking_timeout):
            return func(*args, **kwargs)
        return None

    def get_cache_timeout(self):
        if self.user:
            timeout = self.connection.get(f"{self.user.id} {self.key}")
        else:
            timeout = self.connection.get(self.key)
        if not timeout:
            timeout = self.set_cache_timeout()
        return float(timeout)

    def set_cache_timeout(self):
        obj, create = self.RateLimit.objects.get_or_create(
            api_method=self.key,
            user=self.user,
            system=self.system,
            defaults=dict(limit=self.limit, window=self.window,),
        )
        timeout = round(obj.window / obj.limit, 3)
        if self.user:
            self.connection.set(f"{self.user.id} {self.key}", timeout)
            return timeout
        self.connection.set(self.key, timeout)
        return timeout

    def is_limited(self):
        if self.user:
            lock = Lock(
                redis=self.connection,
                name=f"RateLimiter.request.{self.user.id}.{self.key}.lock",
                timeout=self.get_cache_timeout(),
            )
            return lock.acquire(blocking_timeout=0)

        lock = Lock(
            redis=self.connection,
            name=f"RateLimiter.request.{self.key}.lock",
            timeout=self.get_cache_timeout(),
        )
        return lock.acquire(blocking_timeout=0)

    def limited(self):
        content = {
            "error_description":
                f"Нарушено ограничение на временной интервал между вызовами! "
                f"Действующий интервал: {self.get_cache_timeout() * 1000} мс"
        }
        return Response(content, status=status.HTTP_429_TOO_MANY_REQUESTS)
