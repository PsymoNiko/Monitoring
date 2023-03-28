from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    report_number = models.IntegerField()
    report_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    delayed = models.BooleanField(default=False)
    study_amount = models.CharField(max_length=2)

    # def save(self, *args, **kwargs):
    #     if self.created_at > self.deadline:
    #         self.delayed = True
    #     super().save(*args, **kwargs)
