from django.contrib import admin
from .models import  StudentExerciseModel, MentorExerciseModel
# Register your models here.
# admin.site.register(ExerciseModel)
admin.site.register(StudentExerciseModel)
admin.site.register(MentorExerciseModel)
