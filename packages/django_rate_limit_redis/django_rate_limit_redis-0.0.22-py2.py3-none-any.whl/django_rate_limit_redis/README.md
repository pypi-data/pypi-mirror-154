# Django-Rate-Limit

## Installation

```shell
$ pip install rate_limit
```

### Описание
Django-Rate-Limit - это приложение контроля и ограничения входящих/исходящих запросов,
разработанное для работы в контейнерезированном состоянии, исполюзующее Redis и PostgreSQL как связующее звено.
```Python
rate_limit(
    system=None,  # Имя вашего приложения либо Api константа
    redis_url=None,  # адрес redis
    limit=1,  # разрешенное количество запросов
    window=1,  # временное окно в секундах в котором выполняется разрешенное количество запросов
    blocking_timeout=None,  # время ожидания блокировки исходящих запросов
    request_method=None  # базовый адрес запроса (шаблон урла)
)

```

****

### Логика
При создании входящего/исходящего запроса, берется шаблон урла,
по данному шаблону производится поиск значений настроек в redis, если значение в redis отсутствует,
то поиск производится в БД, в случае если в БД данные остутствуют,
в БД устанавливается значение по умолчанию переданные в декоратор `limit=1, window=1`, после чего производится
сохранение в redis.

Входящие запросы при превышении частоты запросов возвращают `HTTP_429_TOO_MANY_REQUESTS`

Исходящие запросы ожидают окна (выполнение рандомно и не имеет сортировки) для отправки запроса на переданный урл,
время ожидания регулируется именованным аргументом `blocking_timeout`, в случае `None` значения,
ожидание окна будет без временного ограничения.

****
### django-admin
В случае использования администрирования, будет доступен раздел содержащий
в себе настройки ограничений входящих и исходящих запросов


![img.png](img.png)
![img_1.png](img_1.png)

Добавление новых ограничений производится как вручную, так и автоматически при создании входящих/исходящих запросов.
При наличии авторизации в views так же будет учитываться пользователь входящих запросов,
для детальной настройки ограничений. Пользователь для исходящих запросов пока не предусмотрен.

****

# Settings
Необходимо добавить путь к Redis и добавить `rate_limit` в установленные приложения.
```Python
redis_db = 2 # удобная вам БД redis
RATELIMITER_REDIS_URL = f'redis://redis:6379/{redis_db}'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    ...,
    'your_app',
    'rate_limit',
]


```

****

### Примеры
#### Входящие запросы

##### urls.py
```Python
from rate_limit.decorators import rate_limit
from django.urls import path

from . import views

urlpatterns = [
    path('/your-views/', rate_limit(system='api')(views.YourViews.as_view()), name='your-views'),
    path('/more-your-views/', rate_limit(system='api')(views.MoreYourViews.as_view()), name='more-your-views'),
]
```

****

##### views.py
```Python
from rate_limit.decorators import rate_limit
from django.utils.decorators import method_decorator
from rest_framework import generics
from .models import SomeMoreModel
from .serializers import SomeMoreSerializer

@method_decorator(rate_limit(system='api'), name='list')
class SomeMoreYourViews(generics.ListAPIView):
    queryset = SomeMoreModel.objects.all().order_by('-id')
    serializer_class = SomeMoreSerializer
```

****

#### Исходящие запросы
Для исходящих запросов необходимо собрать базовый адрес и передать его как именованный аргумент `method_name`
```Python
import json
import requests
from rate_limit.decorators import rate_limit

@rate_limit(system="your_name_app", request_method="GET")
def request_get(url, headers=None, data=None, params=None, auth=None):
    response = requests.get(url, headers=headers, data=json.dumps(data), params=params, auth=auth)
    return response

@rate_limit(system="your_name_app", request_method="POST")
def request_post(url, headers=None, data=None, params=None, auth=None):
    response = requests.post(url, headers=headers, data=json.dumps(data), params=params, auth=auth)
    return response

your_url = "https://your_url.com/api/"
some_arg = 321

method_name = f"{your_url}" + "{some_arg}/" #  "https://your_url.com/api/{some_arg}/"
response = request_get(f"{your_url}{some_arg}/", method_name=method_name) #  "https://your_url.com/api/321/"
```
Для GET запроса, информация будет сохранена в БД и Redis по ключу `GET https://your_url.com/api/{some_arg}/`
Для POST запроса, информация будет сохранена в БД и Redis по ключу `POST https://your_url.com/api/{some_arg}/`

Так же есть возможность убрать разделение на методы,
убрав именованный аргумент `request_method` у декоратора `@rate_limit`,
в таком случае будет проверяться урл целиком без привязки к методу `https://your_url.com/api/{some_arg}/`
