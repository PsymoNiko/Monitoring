from django.db import models

from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from student.models import Student


class Mentor(models.Model):
    objects = jmodels.jManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')

    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    # password = models.CharField(max_length=128)
    date_of_birth = jmodels.jDateField()
    phone_number = models.CharField(max_length=13, editable=True, unique=True)
    identity_code = models.CharField(max_length=10, unique=True)
    personality = models.CharField(max_length=15, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = False

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
        # return f"{self.id} - {self.first_name} {self.last_name}"
        return f"{self.first_name} - {self.phone_number}"


#exercise

class MentorExerciseModel(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    send_to_all = models.BooleanField(default=False)
    # student_name = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)
    student_name = models.ManyToManyField(Student)
    exercise_name = models.CharField(max_length=200)
    is_seen_by_mentor = models.BooleanField(default=False)
    data_submitted = models.DateField(auto_now_add=True)
    caption = models.TextField()
    exercise_file = models.FileField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.exercise_name


class ExerciseAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exercise = models.ForeignKey(MentorExerciseModel, on_delete=models.CASCADE)


# class ExerciseSubmission(models.Model):
#     # student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     students = models.ManyToManyField(Student, related_name='exercises')
#     exercise = models.ForeignKey(MentorExerciseModel, on_delete=models.CASCADE)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)