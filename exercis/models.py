from django.db import models

from student.models import Student
from mentor.models import Mentor

# class ExerciseModel(models.Model):
#     exercise_name = models.CharField(max_length=200)
#     caption = models.TextField()
#     # exercise_file = models.FileField(upload_to='exercise/', blank=True, null=True)
#     exercise_file = models.FileField(max_length=200, blank=True, null=True)
#     # mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
#     # Students = models.ManyToManyField(Student, through='StudentExerciseModel')
#     students = models.ManyToManyField(Student)
#     """ through?"""
class ExerciseFile(models.Model):
    file = models.FileField(upload_to='exercise_files/', null=True, blank=True)

class StudentExerciseModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exercise_model')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model_student')
    exercise_text = models.TextField(blank=True, null=True)
    exercise_file = models.FileField(max_length=200, blank=True, null=True)
    # exercise_file = models.ForeignKey(ExerciseFile, on_delete=models.SET_NULL, null=True, related_name='s')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_done_exercise = models.BooleanField(default=False)
    # done_exercise = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.exercise_text


class MentorExerciseModel(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model')
    send_to_all = models.BooleanField(default=False)
    # student_name = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)
    student_name = models.ManyToManyField(Student)
    exercise_name = models.CharField(max_length=200)
    is_seen_by_mentor = models.BooleanField(default=False)
    data_submitted = models.DateField(auto_now_add=True)
    caption = models.TextField()
    # exercise_file = models.FileField(max_length=200, blank=True, null=True)
    exercise_file = models.ForeignKey(ExerciseFile, on_delete=models.SET_NULL, null=True, blank=True,related_name='m')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.exercise_name


class ExerciseAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submitte_student')
    exercise = models.ForeignKey(MentorExerciseModel, on_delete=models.CASCADE, related_name='submitte_exercise')
    
    # exercise_name = models.ForeignKey(MentorExerciseModel, on_delete=models.CASCADE, related_name='submitte_exercise_name')
    # exercise_file = models.ForeignKey(MentorExerciseModel, on_delete=models.CASCADE, null=True, blank=True, related_name='submitte_exercise_file')
    # exercise_file = models.FileField(upload_to='exercise_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
   
    # submitted_at = models.DateTimeField(auto_now_add=True)




# class ExerciseSubmission(models.Model):
#     # student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     students = models.ManyToManyField(Student, related_name='exercises')
#     exercise = models.ForeignKey(MentorExerciseModel, on_delete=models.CASCADE)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)