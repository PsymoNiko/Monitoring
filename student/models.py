from django.db import models
from django.contrib.auth.models import User





class Student(models.Model):

    PERSONALITIES = (
        'INTP', 'INTJ', 'ENTJ', 'ENTP',
        'INFJ', 'INFP', 'ENFJ', 'ENFP',
        'ISTJ', 'ISFJ',' ESTJ', 'ESFJ',
        'ISTP', 'ISFP', 'ESTP', 'ESFP',
    )


    student = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35, editable=False)
    last_name = models.CharField(max_length=35, editable=False)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    identity_code = models.IntegerField(editable=False, unique=True)
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)