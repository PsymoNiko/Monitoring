from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from mentor_panel.models import Mentor
from admin_panel.models import Course


class Student(models.Model):
    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_course')
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    phone_number = models.CharField(max_length=13, unique=True)
    date_of_birth = models.DateField()
    identity_code = models.CharField(max_length=15, unique=True)
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['mentor', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CurrentCourse(models.Model):
    belong_to = models.OneToOneField(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=30)
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    course_length = models.IntegerField()
    completed = models.IntegerField()


class CompletedCourses(models.Model):
    course_name = models.CharField(max_length=50)
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    course_length = models.IntegerField()
    started_at = models.DateField()
    finished_at = models.DateField()

    def course_time(self):
        return f"{self.started_at} to {self.finished_at}"


class StudentSettings(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    installment_payment_due_date = models.BooleanField(default=False, editable=True)
    new_task = models.BooleanField(default=False, editable=True)
    new_message = models.BooleanField(default=False, editable=True)


# class Report(models.Model):
#     report_number = models.BigAutoField(default=0)
#     report_text = models.TextField()
#     user = models.OneToOneField(Student, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     deadline = models.DateTimeField()
#     delayed = models.BooleanField(default=False)
#     study_amount = models.CharField(max_length=4)
#
#     # def save(self, *args, **kwargs):
#     #     if self.created_at > self.deadline:
#     #         self.delayed = True
#     #     super().save(*args, **kwargs)
class Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_number = models.IntegerField(default=0)
    text = models.TextField()
    amount_of_study = models.PositiveIntegerField()
    submission_date = models.DateField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)


class Payment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    month_number = models.IntegerField()
    receipt = models.ImageField(upload_to='receipt_images/')
    status = models.CharField(max_length=20, default='pending')


from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import add_unsubmitted_report
