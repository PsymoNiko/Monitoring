from rest_framework import serializers
from .models import StudentExerciseModel,MentorExerciseModel
from student.models import Student
from mentor.models import Mentor
from ceo.models import Course
from .models import Exam, HomeStatusExamModel




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
    # mentor = MentorSerializer(read_only=True)
    class Meta:
        model = Exam
        # fields = '__all__'
        fields = ['mentor', 'exam_name', 'exam_date', 'description', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']



    def create(self, validated_data):
        student_names = validated_data.pop('student_name', [])
        send_to_all = validated_data.pop('send_to_all', False)

        exercise = Exam.objects.create(**validated_data)

        if send_to_all:
            students = Student.objects.all()
            for student in students:
                exercise.send_to_all = True

                exercise.save() 

                exercise.student_name.set(students)

                return exercise






class ExamStatusHomeSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=HomeStatusExamModel.status_choices)
    score = serializers.FloatField()
  

    class Meta:
        model = HomeStatusExamModel
        # fields = '__all__'
        fields = ['exam_name', 'exam_date', 'status', 'score']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']

    def create(self, validated_data):
        mentor_user = self.context['request'].user
        mentor = Mentor.objects.get(user=mentor_user)
        validated_data['mentor'] = mentor
        return super().create(validated_data)
    






















        # def create(self, validated_data):
    #     student_names = validated_data.pop('student_name', [])
    #     send_to_all = validated_data.pop('send_to_all', False)
    #     if send_to_all:
    #         students = Student.objects.all() 
            
    #     else:
    #         students = student_names
            
    #     exercise = MentorExerciseModel.objects.create(**validated_data)
    #     exercise.student_name.set(students)
    #     send_to_all = False
       
    #     return exercise