from django.db import models

from student.models import Student
from mentor.models import Mentor
from ceo.models import Course



class MentorExerciseModel(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model')
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_name')
    student_name = models.ManyToManyField(Student, related_name='assigned_exercises')
    send_to_all = models.BooleanField(default=False)
    exercise_name = models.CharField(max_length=200)
    # is_seen_by_mentor = models.BooleanField(default=False)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.exercise_name


class StudentExerciseModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exercise_model')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model_student')
    exercise_text = models.TextField()
    exercise_file = models.FileField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_done_exercise = models.BooleanField(default=False)
    is_seen_by_mentor = models.BooleanField(default=False)
    

    def __str__(self):
        return self.exercise_text




#exam

class Exam(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exam')
    student_name = models.ManyToManyField(Student, related_name='assigned_exam')
    send_to_all = models.BooleanField(default=False)
    exam_name = models.CharField(max_length=50)
    exam_date = models.DateField()
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.exam_name} - {self.id}"
    


class HomeStatusExamModel(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exam_home')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='home_exam')
    status_choices = [
        ('N', 'Not Held'),
        ('H', 'Held'),
        ('F', 'Finished')
    ]
    status = models.CharField(max_length=1, choices=status_choices, default='N')
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.exam.exam_name} - {self.id}"