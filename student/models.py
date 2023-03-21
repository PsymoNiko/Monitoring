from django.db import models
from django.contrib.auth.models import User

from mentor.models import Mentor


class Student(models.Model):
    PERSONALITIES = (
        ('INTP', 'منطق دان'), ('INTJ', 'معمار'), ('ENTJ', 'فرمانده'), ('ENTP', 'مجادله گر'),
        ('INFJ', 'حامی'), ('INFP', 'میانجی'), ('ENFJ', 'قهرمان'), ('ENFP', 'پیکارگر'),
        ('ISTJ', 'تدارکاتچی'), ('ISFJ', 'مدافع'), ('ESTJ', 'مجری'), ('ESFJ', 'سفیر'),
        ('ISTP', 'چیره دست'), ('ISFP', 'ماجراجو'), ('ESTP', 'کارآفرین'), ('ESFP', 'سرگرم کننده'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    # password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=13, editable=True)
    date_of_birth = models.DateField()
    identity_code = models.IntegerField(unique=True)
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if this is a new student account is being created
        if not self.pk:
            raise Exception("New student account can only be created by an admin.")
        super().save(*args, **kwargs)


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
