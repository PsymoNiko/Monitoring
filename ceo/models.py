from django.db import models
from django.contrib.auth.models import User, Group, Permission

from mentor.models import Mentor

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# class MyUserManager(BaseUserManager):
#     def create_user(self, ):

class Course(models.Model):
    HOLDING = (
        ('Online', 'Online'),
        ('In person', 'In person')
    )

    name = models.CharField(max_length=60)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_of_course')
    start_at = models.DateField()
    duration = models.PositiveSmallIntegerField(default=6)
    class_time = models.TimeField()
    how_to_hold = models.CharField(max_length=15, choices=HOLDING)
    short_brief = models.CharField(max_length=70)


    def __str__(self):
        return self.name

