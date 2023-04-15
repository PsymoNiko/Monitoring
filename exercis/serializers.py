from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel
from student.models import Student
from mentor.models import Mentor
from ceo.models import Course



class MentorExerciseSerializer(serializers.ModelSerializer):
    course_name = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), default=serializers.CurrentUserDefault())


    # student_name = serializers.ListField(child=serializers.IntegerField(), required=False)
    # student_name = serializers.ListField(child=serializers.CharField(max_length=255), required=False)
    def get_queryset(self):
        return Course.objects.filter(owner=self.context['request'].user)

    class Meta:
        model = MentorExerciseModel
        fields = '__all__'


    def create(self, validated_data):
        student_names = validated_data.pop('student_name', [])
        send_to_all = validated_data.pop('send_to_all', False)
        if send_to_all:
            students = Student.objects.all() 
        else:
            students = student_names
            
        exercise = MentorExerciseModel.objects.create(**validated_data)
        exercise.student_name.set(students)
       
        return exercise

    def validate(self, data):
        mentor = self.context['request'].user
        data['mentor'] = mentor
        return data


class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at']


    # def validate(self, data):
    #     student = self.context['request'].user
    #     data['sudent'] = student
    #     return data
    def create(self, validated_data):
        student = self.context['request'].user
        validated_data['student'] = student
        instance = StudentExerciseModel.objects.create(**validated_data)
        return instance
