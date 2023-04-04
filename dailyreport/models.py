from django.db import models
from student.models import Student
from django.urls import reverse

class MentorReportSubmission(models.Model):
    report_number = models.CharField(max_length=50)
    date = models.DateTimeField()
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_hours = models.DecimalField(max_digits=6, decimal_places=2)
    comment = models.TextField(blank=True)
    # is_seen_mentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.report_number} ({self.date})"

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'report_number': self.report_number,
            'caption': self.caption,
            'hours': self.hours,
            'sent': self.sent,
        }
    def get_absolute_url(self):
        return reverse('report_submission_detail', kwargs={'pk': self.pk})




#panel student

class StudentReport(models.Model):
    date = models.DateField()
    report_number = models.IntegerField()
    caption = models.CharField(max_length=255)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    is_send_student = models.BooleanField(default=False)
    is_not_sent_student = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.report_number} ({self.date})"

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'report_number': self.report_number,
            'caption': self.caption,
            'hours': self.hours,
            'sent': self.sent,
        }
