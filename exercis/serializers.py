from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel
from student.models import Student
from mentor.models import Mentor
from ceo.models import Course
# from .models import Exam, HomeStatusExamModel, Grade
from .models import Exam, HomeStatusExamModel, Grade

from student.serializers import StudentSerializer
from ceo.serializers import CourseSerializers


class MentorExerciseSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='MentorStudentExerciseList')
    class Meta:
        model = MentorExerciseModel
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']


    def create(self, validated_data):
        student_names = validated_data.pop('student_name', [])
        send_to_all = validated_data.pop('send_to_all', False)

        if send_to_all:
            students = Student.objects.all()
            send_to_all = True
        else:
            students = student_names
            send_to_all = False

        exercises = []
        for student in students:
            exercise = MentorExerciseModel.objects.create(
                    mentor=validated_data['mentor'],
                    course_name=validated_data['course_name'],
                    exercise_name=validated_data['exercise_name'],
                    caption=validated_data['caption'],
                    send_to_all=send_to_all,
                )
            exercise.student_name.add(student)
            exercises.append(exercise)

        return exercises




    def validate(self, data):
        mentor = self.context['request'].user
        data['mentor'] = mentor
        return data


class StudentExerciseSerializer(serializers.ModelSerializer):
    exercise_text = serializers.CharField(default='')
    class Meta:
        model = StudentExerciseModel
        fields = '__all__'

        read_only_fields = ['created_at', 'modified_at', 'is_deleted']





#exam
class ExamSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Exam
        fields = '__all__'
        # fields = ['mentor', 'exam_name', 'exam_date', 'description', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']


  
    def create(self, validated_data):
        student_names = validated_data.pop('student_name', [])
        send_to_all = validated_data.pop('send_to_all', False)

        if send_to_all:

            students = Student.objects.all()
            send_to_all = True
        else:
            students = student_names
            send_to_all = False

        exams = []
        for student in students:
            # course = validated_data.get('course_name')
            # students = Student.objects.filter(course=course)
            exam_number_count = Exam.objects.filter(student_name=student).count()
            exam = Exam.objects.create(
                    mentor=validated_data['mentor'],
                    # course_name=validated_data['course_name'],
                    exam_name=validated_data['exam_name'],
                    description=validated_data['description'],
                    start_time=validated_data['start_time'],
                    end_time=validated_data['end_time'],
                    # exam_date=validated_data['exam_date'],
                    send_to_all=send_to_all,
                    exam_number=exam_number_count + 1
                    # exam_number=validated_data['exam_number']
                )
            exam.student_name.add(student)
            
            exams.append(exam)

        return exams



class ExamStatusHomeSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=HomeStatusExamModel.status_choices)
    score = serializers.FloatField()
  

    class Meta:
        model = HomeStatusExamModel
        # fields = '__all__'
        fields = ['exam_name', 'exam_date', 'status', 'score', 'exam_number']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']

    
    def create(self, validated_data):
        student = validated_data['student_name']
        exam_number_count = Grade.objects.filter(student=student).count()
        report = Grade.objects.create(exam_number=exam_number_count + 1, **validated_data)
        return report
    
# class GradeSerializer(serializers.ModelSerializer):


class GradeSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student_name.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student_name.last_name', read_only=True)
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    mentor_name = serializers.CharField(source='mentor.name', read_only=True)
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']

# class GradeSerializer(serializers.ModelSerializer):
#     student_name = serializers.StringRelatedField()

#     class Meta:
#         model = Grade
#         fields = ('score', 'opinion', 'student_name')



































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






