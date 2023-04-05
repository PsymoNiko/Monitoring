from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel
from student.models import Student




class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at']



class MentorExerciseSerializer(serializers.ModelSerializer):
    student_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    send_to_all = serializers.BooleanField(default=False)

    class Meta:
        model = MentorExerciseModel
        fields = '__all__'
        # fields = ['mentor', 'send_to_all', 'student_name', 'exercise_name',]
        read_only_fields = ['created_at', 'modified_at']

    def send_to_all(self, obj):
        value = self.context['request'].data.get('send_to_all')
        if value is not None:
            return value.lower() == 'true'
        return False

    # def send_to_all(self, obj):
    #     value = self.context['request'].data.get('send_to_all')
    #     if value is not None:
    #         return bool(value)
    #     return False

    def validate(self, data):
        if not data.get('student_ids') and not data.get('send_to_all'):
            raise serializers.ValidationError('Either student_ids or send_to_all must be provided.')
        if data.get('student_ids') and data.get('send_to_all'):
            raise serializers.ValidationError('Only one of student_ids or send_to_all can be provided.')
        return data





