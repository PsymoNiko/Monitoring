from datetime import date

from django.db import models


class DailyReport(models.Model):
    report_number = models.IntegerField(default=0)
    day_of_report = models.DateField(auto_now_add=True)
    date_field = models.DateField(default=date.today)
    report_text = models.TextField()
    amount_of_study_report = models.CharField(max_length=5)














