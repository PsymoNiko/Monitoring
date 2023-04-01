from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin

from mentor.models import Mentor

from django.contrib.auth.models import UserManager


# class CustomUserManager(UserManager):
#     def create_user(self, username, phone_number=None, identity_code=None, password=None, **extra_fields):
#         # Set the password equal to the identity code
#         username = phone_number
#         password = identity_code
#
#         # Create the user with the updated password
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, identity_code=None, password=None, **extra_fields):
#         # Set the password equal to the identity code
#         password = identity_code
#
#         # Create the superuser with the updated password
#         user = self.create_user(username, identity_code, password, **extra_fields)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     # other fields...
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=('groups'),
#         blank=True,
#         help_text=(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         related_name='user_groups',
#     )


class Student(models.Model):
    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    phone_number = models.CharField(max_length=13, unique=True)
    date_of_birth = models.DateField()
    identity_code = models.CharField(max_length=15, unique=True)
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['mentor', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    # def save(self, *args, **kwargs):
    #     # Check if this is a new student account is being created
    #     if not self.pk:
    #         raise Exception("New student account can only be created by an admin.")
    #     super().save(*args, **kwargs)

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


class Report(models.Model):
    report_number = models.IntegerField(default=0)
    report_text = models.TextField()
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    delayed = models.BooleanField(default=False)
    study_amount = models.CharField(max_length=4)
