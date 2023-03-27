from django.db import models


class DailyReport(models.Model):
    id = models.AutoField(primary_key=True  )
    report_text = models.TextField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

