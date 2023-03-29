from django.db import models


class MentorCommentModel(models.Model):
    comment = models.TextField()


from django.db import models

from django.contrib.auth.models import User, AbstractUser


# class Courses(models.Model):
#     title = models.CharField(max_length=100)
#     course_length = models.IntegerField()
#     completed = models.IntegerField()

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')

    PERSONALITIES = (
        ('INTP', 'منطق دان'), ('INTJ', 'معمار'), ('ENTJ', 'فرمانده'), ('ENTP', 'مجادله گر'),
        ('INFJ', 'حامی'), ('INFP', 'میانجی'), ('ENFJ', 'قهرمان'), ('ENFP', 'پیکارگر'),
        ('ISTJ', 'تدارکاتچی'), ('ISFJ', 'مدافع'), ('ESTJ', 'مجری'), ('ESFJ', 'سفیر'),
        ('ISTP', 'چیره دست'), ('ISFP', 'ماجراجو'), ('ESTP', 'کارآفرین'), ('ESFP', 'سرگرم کننده'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    # password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, editable=True, unique=True)
    identity_code = models.CharField(max_length=10, unique=True)
    personality = models.CharField(max_length=15, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
        return f"{self.id}-{self.first_name} {self.last_name}"
