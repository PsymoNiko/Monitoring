from django.db import models

<<<<<<< HEAD
from django.contrib.auth.models import User,  AbstractUser


# class Courses(models.Model):
#     title = models.CharField(max_length=100)
#     course_length = models.IntegerField()
#     completed = models.IntegerField()

class Mentor(models.Model):


=======
from django.contrib.auth.models import User



class Mentor(models.Model):
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')

    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

<<<<<<< HEAD
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    # password = models.CharField(max_length=128)
=======
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, editable=True, unique=True)
    identity_code = models.CharField(max_length=10, unique=True)
    personality = models.CharField(max_length=15, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

<<<<<<< HEAD
=======
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
<<<<<<< HEAD
        return f"{self.id} - {self.first_name} {self.last_name}"
=======
        # return f"{self.id} - {self.first_name} {self.last_name}"
        return f"{self.first_name} - {self.phone_number} - {self.date_of_birth}"
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
