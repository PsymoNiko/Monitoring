from celery import Celery
from celery.schedules import crontab
# from student_panel.tasks import set_daily_deadline

app = Celery('celery', backend='redis://localhost', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'set_daily_deadline': {
        'task': 'student_panel.tasks.set_daily_deadline',
        'schedule': crontab(hour=22, minute=00, day_of_week=1),
    },
}

app.conf.timezone = 'UTC'

