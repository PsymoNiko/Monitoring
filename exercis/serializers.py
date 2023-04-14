from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel, ExerciseAssignment, ExerciseFile
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
           #fore more than one student
            students = Student.objects.filter(last_name__in=student_names) 
            #for jast one student
            # students = student_names
            
        exercise = MentorExerciseModel.objects.create(**validated_data)
        exercise.student_name.set(students)
       
   
        return exercise




class ExerciseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAssignment
        fields = '__all__'



class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at']