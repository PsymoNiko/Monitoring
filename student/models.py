from django.db import models


class DailyReportModel(models.Model):
    explain_report = models.TextField()
    amount_of_study = models.CharField(max_length=5)
    report_time = models.DateTimeField(auto_now_add=True)
    number_of_report = models.IntegerField(auto_created=True)

    def __str__(self):
        return f"amount of study: {self.amount_of_study}, " \
               f"time of report = {self.report_time}, " \
               f"number 0f report: {self.number_of_report}"








