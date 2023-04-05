from celery import Celery
from celery.schedules import crontab

app = Celery('student_panel',  backend='redis://localhost', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'set_daily_deadline': {
        'task': 'student_panel.tasks.set_daily_deadline',
        'schedule': crontab(hour=23, minute=59),
    },
}

app.conf.timezone = 'UTC'

