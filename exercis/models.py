from django.db import models

from student.models import Student
from mentor.models import Mentor
from ceo.models import Course



from django.core.validators import MaxValueValidator, MinValueValidator




class Exercise(models.Model):

    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model')
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_name')
    student_name = models.ManyToManyField(Student, related_name='assigned_exercises')
    send_to_all = models.BooleanField(default=False)
    exercise_name = models.CharField(max_length=200)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    # exercise_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.exercise_name


class Answer(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exercise')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_exercise')
    exercise_text = models.TextField(blank=False, null=False)
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
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exam')
    student_name = models.ManyToManyField(Student, related_name='assigned_exam')
    send_to_all = models.BooleanField(default=False)
    exam_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    exam_number = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    def __str__(self):
        return {self.exam_name}


class Grade(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_grade')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_grade')
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])
    opinion = models.TextField(max_length=200)
    student_name = models.ManyToManyField(Student, related_name='grade')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.score}"


class AnswerExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_aswer')
    exam_file = models.FileField(max_length=200, blank=True, null=True)
    caption = models.TextField()
    student = models.ManyToManyField(Student, related_name='student_exam')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_answer_exam')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_exam')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

   