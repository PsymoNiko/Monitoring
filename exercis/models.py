from django.db import models
# from django.contrib.auth.models import User
from student.models import Student
from mentor.models import Mentor

class ExerciseModel(models.Model):
    exercise_name = models.CharField(max_length=200)
    caption = models.TextField()
    exercise_file = models.FileField(upload_to='exercise/', blank=True, null=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    Student = models.ManyToManyField(Student, through='StudentExerciseModel')


class StudentExerciseModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # caption = models.CharField(max_length=500)
    exercises = models.ForeignKey(ExerciseModel, on_delete=models.CASCADE)
    exercise_text = models.TextField(blank=True, null=True)
    exercise_file = models.FileField(upload_to='exercise/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    done_exercise = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.caption


# class MentorExerciseModel(models.Model):
#     # student_name = models.CharField(max_length=100)
#     student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
#     # exercise_name = models.CharField(max_length=100)
#     exercise_name = models.ForeignKey(ExerciseModel,on_delete=models.CASCADE)
#     is_seen_by_teacher = models.BooleanField(default=False)
#     data_submitted = models.DateField()