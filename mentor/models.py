from django.db import models

from django.contrib.auth.models import User,  AbstractUser


# class Courses(models.Model):
#     title = models.CharField(max_length=100)
#     course_length = models.IntegerField()
#     completed = models.IntegerField()

class Mentor(AbstractUser):
    PERSONALITIES = (
        ('منطق دان', 'INTP'), ('INTJ', 'معمار'), ('ENTJ', 'فرمانده'), ('ENTP', 'مجادله گر'),
        ('INFJ', 'حامی'), ('INFP', 'میانجی'), ('ENFJ', 'قهرمان'), ('ENFP', 'پیکارگر'),
        ('ISTJ', 'تدارکاتچی'), ('ISFJ', 'مدافع'), ('ESTJ', 'مجری'), ('ESFJ', 'سفیر'),
        ('ISTP', 'چیره دست'), ('ISFP', 'ماجراجو'), ('ESTP', 'کارآفرین'), ('ESFP', 'سرگرم کننده'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    # password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, editable=True)
    identity_code = models.CharField(max_length=10, unique=True)
    personality = models.CharField(max_length=15, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    USERNAME_FIELD = 'identity_code'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']


# second_item = [PERSONALITY[1] for PERSONALITY in PERSONALITIES]

# def save(self, *args, **kwargs):
#     if not self.pk:
#         raise Exception("New mentor account can only be created by an admin")
#     super().save(*args, **kwargs)

# def full_name(self):
#     return f"{self.first_name} {self.last_name}"
#
# def courses(self):
#     courses = models.ForeignKey(Courses, on_delete=models.CASCADE)

# class CurrentCourse(models.Model):
#     courses = models.ForeignKey(Mentor, on_delete=models.CASCADE)
#     course_name = models.CharField(max_length=30)
#     course_length = models.IntegerField()
#     completed = models.IntegerField()
