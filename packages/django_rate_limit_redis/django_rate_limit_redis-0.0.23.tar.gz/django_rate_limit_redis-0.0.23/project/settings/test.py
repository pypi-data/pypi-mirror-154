from .base import *  # noqa

ENV_TYPE = 'test'
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

ELASTIC_APM = {
    'DISABLE_SEND': True,
}

DISABLE_REPLICA = True

STATSD_ENABLED = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'keyring.backend': {
            'handlers': ['console'],
            'level': 'CRITICAL',
        },
        'elasticapm': {
            'handlers': ['console'],
            'level': 'CRITICAL',
        },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    }
}
