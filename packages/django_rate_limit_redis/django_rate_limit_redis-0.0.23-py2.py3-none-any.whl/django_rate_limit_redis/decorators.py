from functools import wraps

from django_rate_limit_redis.core import RedisRateLimiter

API = 'API'


def rate_limit(system=None, redis_url=None, limit=1, window=1, blocking_timeout=None, request_method=None):
    '''
    :param system: Имя вашего приложения либо константа 'Api'
    :param redis_url: Адрес redis
    :param limit: Разрешенное количество запросов
    :param window: Временное окно в секундах в котором выполняется разрешенное количество запросов
    :param blocking_timeout: Время ожидания блокировки исходящих запросов
    :param request_method: Базовый адрес запроса (шаблон урла)
    :return: response
    '''
    def decorator(func):
        if system == API or system.upper() == API:
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                request_method = request.method
                user = request.user
                url_pattern = str(request.resolver_match.route)
                method_name = f"{request_method} {url_pattern}"
                redis_ratelimiter = RedisRateLimiter(
                    system=system,
                    key=method_name,
                    redis_url=redis_url,
                    limit=limit,
                    window=window,
                    blocking_timeout=blocking_timeout,
                    user=user
                )
                is_limited = redis_ratelimiter.is_limited()
                if is_limited:
                    return func(request, *args, **kwargs)
                return redis_ratelimiter.limited()
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                method_name = kwargs.get("method_name")
                if method_name:
                    kwargs.pop("method_name")
                if not method_name:
                    method_name = args[0].base_url
                if method_name:
                    if request_method:
                        method_name = f"{request_method} {method_name}"

                    return RedisRateLimiter(
                        system=system,
                        key=method_name,
                        redis_url=redis_url,
                        limit=limit,
                        window=window,
                        blocking_timeout=blocking_timeout,
                    ).redis_rate_limit(func, *args, **kwargs)
                else:
                    return func(*args, **kwargs)
        return wrapper

    return decorator
