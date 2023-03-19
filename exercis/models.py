from django.db import models
# from django.contrib.auth.models import User
from student.models import Student




class ExerciseModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    caption = models.CharField(max_length=500)
    exercise_text = models.TextField()
    exercise_file = models.FileField(upload_to='exercise/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.caption

