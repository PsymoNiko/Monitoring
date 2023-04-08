from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel, ExerciseAssignment, ExerciseFile
from student.models import Student




class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at']

class MentorExerciseSerializer(serializers.ModelSerializer):
    # student_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    send_to_all = serializers.BooleanField(default=False)
    # student_name = serializers.CharField(max_length=200, required=False)
    student_names = serializers.ListField(child=serializers.CharField(), required=False)

    exercise_file = serializers.FileField(required=False)
    class Meta:
        model = MentorExerciseModel
        fields = '__all__'
        # fields = ['mentor', 'send_to_all', 'student_name', 'exercise_name','student', 'is_seen_by_mentor', '']
        read_only_fields = ['created_at', 'modified_at']

    def send_to_all(self, obj):
        value = self.context['request'].data.get('send_to_all')
        if value is not None:
            return value.lower() == 'true'
        return False

    def validate(self, data):
        student_name = data.get('student_name')
        send_to_all = data.get('send_to_all')

        if not student_name and not send_to_all:
            raise serializers.ValidationError('Either student_name or send_to_all must be provided.')
        if student_name and send_to_all:
            raise serializers.ValidationError('Only one of student_name or send_to_all can be provided.')

        return data


    def create(self, validated_data):
        exercise_file = validated_data.pop('exercise_file', None)
        if exercise_file:
            exercise_file_obj = ExerciseFile.objects.create(file=exercise_file)
            validated_data['exercise_file_id'] = exercise_file_obj.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        exercise_file = validated_data.pop('exercise_file', None)
        if exercise_file:
            exercise_file_obj = ExerciseFile.objects.create(file=exercise_file)
            validated_data['exercise_file_id'] = exercise_file_obj.id
        return super().update(instance, validated_data)


class ExerciseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAssignment
        fields = '__all__'







