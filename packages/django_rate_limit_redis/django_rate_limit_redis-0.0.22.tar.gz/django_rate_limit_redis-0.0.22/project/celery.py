import logging
import os

from celery import Celery

from django.conf import settings

logger = logging.getLogger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

DEFAULT_QUEUE = "default"

CELERY_APP_QUEUES_CHOICES = (
    (DEFAULT_QUEUE, "Очередь по-умолчанию"),
)

ROUTES = {
    # DEFAULT: (
    #     "core.tasks.send_all_nomenclature",
    # ),
}


def get_task_routes():
    return {task: {"queue": queue} for queue, tasks in ROUTES.items() for task in tasks}


app = Celery("app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.conf.update(
    task_routes=get_task_routes(),
    task_default_queue=DEFAULT_QUEUE,
    result_expires=1 * 60 * 60,  # 1 hour
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
