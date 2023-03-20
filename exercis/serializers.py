from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel



class StudentExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'



class MentorExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorExerciseModel
        fields = '__all__'

        