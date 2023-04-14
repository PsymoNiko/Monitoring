import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from mentor.models import Mentor
from ceo.models import Course


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

    # objects = CustomUserManager()

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = False

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
    """
    For turn on/off the sms panel for each student
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    installment_payment_due_date = models.BooleanField(default=False, editable=True)
    new_task = models.BooleanField(default=False, editable=True)
    new_message = models.BooleanField(default=False, editable=True)


class Payment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    month_number = models.IntegerField()
    receipt = models.ImageField(upload_to='receipt_images/')
    status = models.CharField(max_length=20, default='pending')


class Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_text = models.TextField()
    study_amount = models.FloatField()
    report_number = models.IntegerField()
    is_submitted = models.BooleanField(default=False)
    time_of_submit = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    # deadline = models.DateTimeField(default=datetime.datetime.)
    #
    # @property
    # def delay(self):
    #     if self.is_submitted:
    #         if self.time_of_submit <= self.deadline:
    #             return datetime.timedelta()
    #         else:
    #             return self.time_of_submit - self.deadline
    #     else:
    #         return None








