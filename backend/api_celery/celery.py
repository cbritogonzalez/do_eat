
from celery import Celery
from celery.schedules import crontab

import json

app = Celery('api_celery',include=['api_celery.tasks'])
app.config_from_object('api_celery.celeryconfig')

app.conf.beat_schedule = {
    "schedule_fetch_AH": {
        "task": "api_celery.tasks.fetch_albert_heijn",
        # "schedule": 300.0
        "schedule": crontab(minute="*/5")
    },
    "schedule_fetch_jumbo": {
        "task": "api_celery.tasks.fetch_jumbo",
        # "schedule": 300.0
        "schedule": crontab(minute="*/5")
    },
}

# celery -A api_celery worker --loglevel=info --pool=solo
# celery -A api_celery worker --loglevel=info --pool=solo --concurrency=2
# celery -A api_celery beat --loglevel=info
# Celery -P threads or --pool=solo options solves the issue.