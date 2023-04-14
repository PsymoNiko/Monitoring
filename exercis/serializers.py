from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel, ExerciseAssignment, ExerciseFile
from student.models import Student






class MentorExerciseSerializer(serializers.ModelSerializer):
    # send_to_all = serializers.BooleanField(default=False)
    # student_names = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = MentorExerciseModel
        # fields = '__all__'
        fields = ['mentor','course_name', 'student_name', 'send_to_all', 'exercise_name', 'caption']
        read_only_fields = ['created_at', 'modified_at', 'is_seen_by_mentor','is_deleted']
# 
    # def send_to_all(self, obj):
    #     value = self.context['request'].data.get('send_to_all')
    #     if value is not None:
    #         return value.lower() == 'true'
    #     return False

    # def validate(self, data):
    #     student_name = data.get('student_name')
    #     send_to_all = data.get('send_to_all')

    #     if not student_name and not send_to_all:
    #         raise serializers.ValidationError('Either student_name or send_to_all must be provided.')
    #     if student_name and send_to_all:
    #         raise serializers.ValidationError('Only one of student_name or send_to_all can be provided.')

    #     return data


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