from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .management import create_permissions


class UsersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи и группы'

    def ready(self):
        post_migrate.connect(
            create_permissions,
            dispatch_uid="users.management.create_permissions"
        )
