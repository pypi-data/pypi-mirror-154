import redis

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

Users = get_user_model()


class RateLimit(models.Model):
    system = models.CharField("Система", max_length=50)

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=("Пользователь"),
    )

    api_method = models.CharField(
        "API метод",
        max_length=255,
        help_text=("<strong>Пример:</strong>" " <em>GET https://demo.pharm-zakaz.ru/api/distributor/v1/stores/</em>"),
        blank=True,
    )
    limit = models.IntegerField(
        "Количество запросов",
        help_text="Максимальное количество запросов за временной интервал",
        null=True,
        blank=True,
    )
    window = models.IntegerField(
        "Временной интервал в секундах",
        help_text="Интервал в котором будут считаться запросы для limit",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        timeout = round(self.window / self.limit, 3)
        connection = redis.from_url(settings.RATELIMITER_REDIS_URL)
        if self.user:
            connection.set(f"{self.user.id} {self.api_method}", timeout)
        else:
            connection.set(self.api_method, timeout)
        super(RateLimit, self).save(*args, **kwargs)
