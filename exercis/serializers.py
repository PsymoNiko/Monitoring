from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel
from student.models import Student




class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'



class MentorExerciseSerializer(serializers.ModelSerializer):
    student_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    send_to_all = serializers.BooleanField(default=False)

    class Meta:
        model = MentorExerciseModel
        fields = '__all__'

    # def validate_student_ids(self, value):
    #     if not value:
    #         raise serializers.ValidationError('At least one student must be selected')
    #     elif not Student.objects.filter(id__in=value).exists():
    #         raise serializers.ValidationError('Invalid student ID')
    #     return value

    # def validate(self, data):
    #     if not data.get('send_to_all') and not data.get('student_ids'):
    #         raise serializers.ValidationError("Either 'send_to_all' or 'student_ids' must be specified")
    #     return data
    def get_send_to_all(self, obj):
        value = self.context['request'].data.get('send_to_all')
        if value is not None:
            return bool(value)
        return False

    def validate(self, data):
        if not data.get('student_ids') and not data.get('send_to_all'):
            raise serializers.ValidationError('Either student_ids or send_to_all must be provided.')
        if data.get('student_ids') and data.get('send_to_all'):
            raise serializers.ValidationError('Only one of student_ids or send_to_all can be provided.')
        return data



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



