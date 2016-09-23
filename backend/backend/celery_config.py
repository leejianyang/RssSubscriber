# -*- coding:utf-8 -*-
from datetime import timedelta


BROKER_URL = 'redis://127.0.0.1/13'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1/13'
CELERYBEAT_SCHEDULE = {
    'update_feeds': {
        'task': 'task.main_task',
        'schedule': timedelta(minutes=30)
    }
}