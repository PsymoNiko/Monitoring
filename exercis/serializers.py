from rest_framework import serializers
from .models import Answer,Exercise
from student.models import Student
from mentor.models import Mentor
from ceo.models import Course

from .models import Exam, Grade, AnswerExam



class ExerciseSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='MentorStudentExerciseList')
    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']
     

    def validate(self, data):
    
        mentor = self.context['request'].user
        data['mentor'] = mentor
        return data



class AnswerSerializer(serializers.ModelSerializer):
    # exercise_text = serializers.CharField(default='')
    class Meta:
        model = Answer
        fields = '__all__'

        read_only_fields = ['created_at', 'modified_at', 'is_deleted', 'mentor', 'student','course', 'exercise']
        extra_kwargs = {
            'exercise_text': {'required': True},
        }



#exam
class ExamSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Exam
        fields = '__all__'
        # fields = ['mentor', 'exam_name', 'exam_date', 'description', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted', 'course_name']



class GradeSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student_name.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student_name.last_name', read_only=True)
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    mentor_name = serializers.CharField(source='mentor.name', read_only=True)
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'is_deleted', 'exam', 'mentor', 'student_name']


class ExamStatusHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
        # fields = ['exam_name', 'exam_date', 'status', 'score', 'exam_number']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']


class AnswerExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerExam
        fields = '__all__'
        # fields = ['exam_name', 'exam_date', 'status', 'score', 'exam_number']
        read_only_fields = ['exam','mentor','course', 'created_at', 'modified_at', 'is_deleted']





























    # student_first_name = serializers.CharField(source='student_name.first_name', read_only=True)
    # student_last_name = serializers.CharField(source='student_name.last_name', read_only=True)
    # exam_name = serializers.CharField(source='exam.id', read_only=True)
    # class Meta:
    #     model = Grade
    #     # fields = ['id', 'score', 'opinion','student_name']
    #     fields = ['id', 'score','exam_name', 'opinion', 'student_name','student_first_name', 'student_last_name']

    #     read_only_fields = ['created_at', 'modified_at', 'is_deleted','mentor','exam',]

   
    # def create(self, validated_data):
    #     student_names = validated_data.pop('student_name', [])
    #     students = student_names
        
    #     grades = []
    #     for student in students:
    #         # exam_number_count = Exam.objects.filter(student_name=student).count()
    #         grade = Grade.objects.create(
    #                 mentor=validated_data['mentor'],
    #                 # course_name=validated_data['course_name'],
    #                 # exam=validated_data['exam'],
    #                 opinion=validated_data['opinion'],
    #                 score=validated_data['score'],
                
    #             )
    #         grade.student_name.add(student)
            
    #         grades.append(grade)

    #     return grades






