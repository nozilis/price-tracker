from __future__ import absolute_import, unicode_literals
from decouple import config
from celery import Celery
from celery.schedules import crontab

app = Celery('price_tracker')
app.conf.broker_url = config('BROKER_URL')
app.conf.result_backend = config('BROKER_URL')
app.conf.beat_schedule = {
    "price-checking-every-day": {
        "task": "tasks.price_check",
        "schedule": crontab(hour="0", minute="0"),  
    },
}

app.conf.timezone = "UTC"

app.autodiscover_tasks()