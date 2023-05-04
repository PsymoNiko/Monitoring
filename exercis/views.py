from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import get_object_or_404
import datetime


from .models import(
     Exercise,
     Answer,
     Exam,
     Grade,
     AnswerExam
)

from .serializers import (
    AnswerSerializer, 
    ExerciseSerializer,
    ExamSerializer,
    ExamStatusHomeSerializer,
    GradeSerializer,
    AnswerExamSerializer
   
)
from ceo.models import Course
from student.models import Student
from mentor.models import Mentor
# from redis import Redis
# from django.core.cache import cache

from rest_framework import generics



# redis_client = Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

class MentorSendExercise(APIView):

   #   authentication_classes = [JWTAuthentication]
    def post(self, request, course_id):
        serializer = ExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor = Mentor.objects.get(user=request.user)
        # courses = mentor.mentor_of_course.all()
        # print(courses)
        # courses = Course.objects.filter()
        student_names = serializer.validated_data.pop('student_name', [])
        send_to_all = serializer.validated_data.pop('send_to_all', False)

        if send_to_all:
            students =  Student.objects.filter(course=course_id)
            send_to_all = True
        else:
            student_ids = [student.id for student in student_names]
            students = Student.objects.filter(id__in=student_ids, course=course_id)
            for student_id in student_ids:
                if not Student.objects.filter(id=student_id, course=course_id).exists():
                    raise ValidationError(f"Student with id {student_id} is not enrolled in the course {course_id}")
            send_to_all = False

        exercises = []
        for student in students:

            exercise = serializer.save(
                mentor=mentor,
                send_to_all=send_to_all,
            )
            exercise.student_name.add(student)
            exercises.append(exercise)

        response_data = []
        for exercise in exercises:
            response_data.append(serializer.to_representation(exercise))
        return Response(response_data, status=status.HTTP_201_CREATED)



class GetPostedExerciseOfMentor(APIView):
#   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id):
        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = Exercise.objects.filter(mentor=mentor, student_name=student)
        serializer = ExerciseSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOnePostedExerciseOfMentor(APIView):
#   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id, id ):
        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = Exercise.objects.filter(mentor=mentor, student_name=student, id=id)
        serializer = ExerciseSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



#get exercise of student
class MentorStudentExerciseList(APIView):
 #   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id):

        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = Answer.objects.filter(mentor=mentor, student=student, is_done_exercise=True)
        for exercise in exercises:
            exercise.is_seen_by_mentor = True
            exercise.save()
        serializer = AnswerSerializer(exercises, many=True)
        return Response(serializer.data)


class GetMentorExerciseStatus(APIView):
 #   authentication_classes = [JWTAuthentication]

    def get(self, request, student_id):
        mentor = Mentor.objects.get(user=request.user)
        
        student = Student.objects.get(id=student_id)

        exercises_viewed = Answer.objects.filter(mentor=mentor,  student=student, is_seen_by_mentor=True)
        exercises_not_viewed = Answer.objects.filter(mentor=mentor,  student=student, is_seen_by_mentor=False)
        num_exercises_viewed = exercises_viewed.count()
        num_exercises_not_viewed = exercises_not_viewed.count()
        return Response({'num_exercises_viewed': num_exercises_viewed, 'num_exercises_not_viewed': num_exercises_not_viewed})
    
#student

class StudentPanelSendExercise(APIView):
#   authentication_classes = [JWTAuthentication]


    def get_object(self, id):
        mentor = Student.objects.get(user=self.request.user)
        return Exercise.objects.filter(id=id, student_name=mentor)

    def get(self, request, id, format=None):
        exercise = self.get_object(id)
        serializer = ExerciseSerializer(exercise, many=True)
        return Response(serializer.data)
    

    def post(self,request, id):
        student = Student.objects.get(user=request.user)

        exercise =Exercise.objects.get(id=id, student_name=student)

        # print(student.course)
        course = student.course
        mentor = course.mentor
        exercise = Exercise.objects.get(id=id, student_name=student)

        # Check if the student has already answered the exercise
        if Answer.objects.filter(student=student, exercise=exercise, is_done_exercise=True).exists():
            return Response({'detail': 'You have already answered this exercise.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the course object has the id attribute
        if not hasattr(course, 'id'):
            course = Course.objects.get(pk=course.pk)

        serializer = AnswerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(student=student, mentor=mentor,course=course, exercise=exercise)   
        instance.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetPostedExerciseOfStudent(APIView):
   #   authentication_classes = [JWTAuthentication]

    def get(self, request, id):
  
        student = Student.objects.get(user=request.user)
        exercises_done = Answer.objects.filter(student=student)
        exercise=Exercise.objects.filter(id=id)
        exercises_done.update(is_done_exercise=False)
        serializer = AnswerSerializer(instance=exercises_done, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetStudentExerciseStatus(APIView):
#   authentication_classes = [JWTAuthentication]
 
    def get(self, request, *args, **kwargs):

        student = Student.objects.get(user=request.user)
        exercises_done = Answer.objects.filter(student=student, is_done_exercise=True)
        exercises_not_done = Answer.objects.filter(student=student, is_done_exercise=False)
        num_exercises_done = exercises_done.count()
        num_exercises_not_done = exercises_not_done.count()
        return Response({'num_exercises_done': num_exercises_done, 'num_exercises_not_done': num_exercises_not_done})





#exam

class MentorCreateExam(APIView):
    
    def post(self, request, course_id):
        serializer = ExamSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor = Mentor.objects.get(user=request.user)
        student_names = serializer.validated_data.pop('student_name', [])
        send_to_all = serializer.validated_data.pop('send_to_all', False)

        if send_to_all:
            # students = Student.objects.all()
            students =  Student.objects.filter(course=course_id)
            send_to_all = True
        else:
            student_ids = [student.id for student in student_names]
            students = Student.objects.filter(id__in=student_ids, course=course_id)
            for student_id in student_ids:
                if not Student.objects.filter(id=student_id, course=course_id).exists():
                    raise ValidationError(f"Student with id {student_id} is not enrolled in the course {course_id}")
            send_to_all = False

        

        exams = []
        for student in students:
            exam_number_count = Exam.objects.filter(student_name=student).count()
            exam = serializer.save(
                mentor=mentor,
                send_to_all=send_to_all,
                exam_number=exam_number_count + 1,
                course_name_id=course_id
            )
            # exam.student_name.set([student])
            exam.student_name.add(student)
            exams.append(exam)

        response_data = []
        for exam in exams:
            response_data.append(serializer.to_representation(exam))
        return Response(response_data, status=status.HTTP_201_CREATED)


class GetAllExam(APIView):
    def get_object(self, exam_id):
        mentor = Mentor.objects.get(user=self.request.user)
        return Exam.objects.filter(id=exam_id, mentor=mentor)

    def get(self, request, exam_id, format=None):
        exams = self.get_object(exam_id)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)



class AddGradeView(APIView):
    # def get_object(self, id):
    #     mentor = Mentor.objects.get(user=self.request.user)
    #     return AnswerExam.objects.filter(id=id, mentor=mentor)

    # def get(self, request, id, format=None):
        
    #     answer = self.get_object(id)
    #     serializer = AnswerExamSerializer(answer)
    #     return Response(serializer.data)

    def post(self, request, exam_id, student_id):
        mentor = Mentor.objects.get(user=request.user)
        exam = Exam.objects.get(id=exam_id, mentor=mentor)
        student = Student.objects.get(id=student_id)

        # Check if the student has submitted an answer to the exam
        if not AnswerExam.objects.filter(student=student, exam=exam).exists():
            return Response({'detail': 'This student has not submitted an answer for this exam.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the exam has already been graded for this student
        if Grade.objects.filter(exam=exam, student_name=student).exists():
            return Response({'detail': 'This exam has already been graded for this student.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GradeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(mentor=mentor, exam=exam, student_name=[student])
        return Response(serializer.data, status=status.HTTP_201_CREATED)












    # def post(self, request, id):
    #     answer = self.get_object(id)
    #     # answer = AnswerExam.objects.get(id=id)

    #     # student = Student.objects.get(id=student_id)
    #     student = answer.student
    #     exam = answer.exam

    #     # print(student)
    #     if not answer :
    #         return Response({"detail": "answer not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     mentor = Mentor.objects.get(user=request.user)
    #     serializer = GradeSerializer(data=request.data, context={'request': request, 'exam': exam})
    #     serializer.is_valid(raise_exception=True)
    #     # serializer.save(mentor=mentor, student_name=student, exam=exam)
    #     grade = serializer.save(mentor=mentor, exam=exam)
    #     grade.student_name.add([student])


    #     return Response(grade, status=status.HTTP_201_CREATED)




class GradeListView(APIView):
   
    def get(self, request, exam_id):
        mentor = Mentor.objects.get(user=request.user)
        exam = Exam.objects.filter(id=exam_id, mentor=mentor)
        grades = Grade.objects.all()

        if exam:
            grades = Grade.objects.filter(mentor=mentor)
            serializer = GradeSerializer(grades, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class ExamStatusList(generics.ListAPIView):
    queryset = Exam.objects.filter(is_deleted=False)
    serializer_class = ExamStatusHomeSerializer

    def get(self, request, *args, **kwargs):
        exams = self.get_queryset()
        serializer = self.get_serializer(exams, many=True)
        status_list = []
        for exam in exams:
            status = self.get_exam_status(exam)
            status_list.append({
                'exam_id': exam.id,
                'exam_name': exam.exam_name,
                'status': status,
                'start_time': exam.start_time,
                'end_time': exam.end_time

            })
        return Response(status_list)

    def get_exam_status(self, exam):
        # Get the current datetime in UTC timezone
        current_datetime = datetime.datetime.now(datetime.timezone.utc)
        # Add 3.5 hours to the current datetime
        now = current_datetime + datetime.timedelta(hours=3, minutes=30)
        # print(now)
        if exam.start_time <= now < exam.end_time:
            return 'Holding'
        elif exam.end_time <= now:
            return 'Completed'
        else:
            return 'Not held'



#student

class StudentGetExam(APIView):
#   authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        # mentor = Mentor.objects.get(user=self.request.user)
        student = Student.objects.get(user=self.request.user)
        return Exam.objects.filter(id=id, student_name=student)

    def get(self, request, id, format=None):
        exams = self.get_object(id)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self,request, id):
        student = Student.objects.get(user=request.user)

        exam =Exam.objects.get(id=id, student_name=student)

        # print(student.course)
        course = student.course
        mentor = course.mentor
        # mentor = Mentor.objects.get()

        # Check if the student has already answered the exercise
        if AnswerExam.objects.filter(student=student, exam=exam).exists():
            return Response({'detail': 'You have already answered this exercise.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the course object has the id attribute
        if not hasattr(course, 'id'):
            course = Course.objects.get(pk=course.pk)

        serializer = AnswerExamSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(student=[student], mentor=mentor,course=course, exam=exam)   
        # instance.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class GradeView(APIView):
   
    def get(self, request, exam_id):
        # mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(user=request.user)
        try:
        # exam = Exam.objects.filter(id=exam_id, student_name=student)
            grade = Grade.objects.get(exam_id=exam_id, student_name=student)
            serializer = GradeSerializer(grade)
            return Response(serializer.data)
        except Grade.DoesNotExist:
            return Response({'detail': 'Grade not found.'}, status=status.HTTP_404_NOT_FOUND)
        # if exam:
        #     grades = Grade.objects.filter(student_name=student)
        #     serializer = GradeSerializer(grades, many=True)
        #     return Response(serializer.data)
        # else:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

























































































# class StudentPanelSendExercise(APIView):
#     # serializer_class = StudentExerciseSerializer

#     # def get_serializer(self, *args, **kwargs):
#     #     return self.serializer_class(*args, **kwargs)
#     # authentication_classes = [TokenAuthentication]  
#     # permission_classes = [IsAuthenticated]

#     def post(self,request, *args, **kwargs):

#         serializer = StudentExerciseSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         exercise_s = serializer.save()
    
#         redis_key_student= exercise_s.id
#         redis_client.set(redis_key_student, json.dumps(serializer.data))
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    


# class GetPostedExerciseOfStudent(APIView):
#     # authentication_classes = [TokenAuthentication]  
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
        
#         exercises_s = []
#         for exercise in  MentorExerciseModel.objects.all():
#             redis_key_student = exercise.id
#             exercise_json = redis_client.get(redis_key_student)
        
#             if exercise_json is not None:
#               exercises_s.append(json.loads(exercise_json))
         
#         return Response(exercises_s, status=status.HTTP_200_OK)





# redis
# class GetPostedExerciseOfMentor(APIView):
    # authentication_classes = [TokenAuthentication]  

    # def get(self, request, *args, **kwargs):
     
    #     exercises = []
    #     for exercise in  MentorExerciseModel.objects.all():
    #         redis_key = exercise.id
    #         exercise_json = redis_client.get(redis_key)
        
    #         if exercise_json is not None:
    #           exercises.append(json.loads(exercise_json))
         
    #     return Response(exercises, status=status.HTTP_200_OK)