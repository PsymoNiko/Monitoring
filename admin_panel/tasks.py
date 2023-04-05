# from requests import get
# from celery import Celery
# from .models import LeaveDurationModel
#
# app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')
#
#
# @app.task
# def leave_duration_left(instance):
#     response_of_set_leave_time = get('http://127.0.0.1:8000/set-leave-time/')
#     leave_duration = response_of_set_leave_time.json()['leave_duration']
#
#     leave_period = LeaveDurationModel.leave_duration
#
#     duration_left = (int(leave_duration) - int(leave_period))
#
#     return duration_left
