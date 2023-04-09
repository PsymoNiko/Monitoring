from django.db import models

from django.contrib.auth.models import User



class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')

    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, editable=True, unique=True)
    identity_code = models.CharField(max_length=10, unique=True)
    personality = models.CharField(max_length=15, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
        # return f"{self.id} - {self.first_name} {self.last_name}"
        return f"{self.first_name} - {self.phone_number} - {self.date_of_birth}"
