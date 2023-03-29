from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel, ExerciseModel
from student.models import Student




class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'



class MentorExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorExerciseModel
        fields = '__all__'

        # def create(self, validated_data):
        #     student_id = validated_data.pop('student_id')
        #     exercise_text = validated_data.pop('exercise')

        #     student = Student.objects.get(id=student_id)
        #     exercise = ExerciseModel.objects.create(student=student, exercise_text=exercise_text)
        #     unseen_count = student.exercises.filter(seen=False).count()
        #     seen_count = student.exercises.filter(seen=True).count()
        #     student.unseen_count = unseen_count
        #     student.seen_count = seen_count
        #     student.save()
        #     return exercise



