from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Courses(models.Model):
    title = models.CharField(max_length=100)
    course_length = models.IntegerField()
    completed = models.IntegerField()

class Mentor(models.Model):
    PERSONALITIES = (
        'INTP', 'INTJ', 'ENTJ', 'ENTP',
        'INFJ', 'INFP', 'ENFJ', 'ENFP',
        'ISTJ', 'ISFJ', ' ESTJ', 'ESFJ',
        'ISTP', 'ISFP', 'ESTP', 'ESFP',
    )

    mentor = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35, editable=False)
    last_name = models.CharField(max_length=35, editable=False)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, editable=True)
    identity_code = models.IntegerField(editable=False, unique=True)
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def courses(self):
        courses = models.ForeignKey(Courses, on_delete=models.CASCADE)


class CurrentCourse(models.Model):
    courses = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=30)
    course_length = models.IntegerField()
    completed = models.IntegerField()
