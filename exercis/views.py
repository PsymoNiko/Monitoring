from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



from .models import(
     StudentExerciseModel,
     MentorExerciseModel,
     HomeStatusExamModel,
     Exam
)

from .serializers import (
    StudentExerciseSerializer, 
    MentorExerciseSerializer,
    ExamSerializer,
    ExamStatusHomeSerializer,
    
)

from student.models import Student
from mentor.models import Mentor
from redis import Redis
import json
from django.core.cache import cache


redis_client = Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

class MentorPanelSendExercise(APIView):

   #   authentication_classes = [JWTAuthentication]


    def post(self,request, *args, **kwargs):
        serializer = MentorExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor = Mentor.objects.get(user=request.user)
      
        exercises = serializer.save(mentor=mentor)

        response_data = []
        for exercise in exercises:
            response_data.append(serializer.to_representation(exercise))

        return Response(response_data, status=status.HTTP_201_CREATED)



class GetPostedExerciseOfMentor(APIView):
#   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id):

        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)

        # exercises = MentorExerciseModel.objects.all()
        exercises = MentorExerciseModel.objects.filter(mentor=mentor, student_name=student)
    
        serializer = MentorExerciseSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MentorStudentExerciseList(APIView):
 #   authentication_classes = [JWTAuthentication]

    def get(self, request,  student_id):

        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = StudentExerciseModel.objects.filter(mentor=mentor, student=student, is_done_exercise=True)
        for exercise in exercises:
            exercise.is_seen_by_mentor = True
            exercise.save()
        serializer = StudentExerciseSerializer(exercises, many=True)
        return Response(serializer.data)


class GetMentorExerciseStatus(APIView):
 #   authentication_classes = [JWTAuthentication]

    def get(self, request, student_id):
        mentor = Mentor.objects.get(user=request.user)
        
        student = Student.objects.get(id=student_id)

        exercises_viewed = StudentExerciseModel.objects.filter(mentor=mentor,  student=student, is_seen_by_mentor=True)
        exercises_not_viewed = StudentExerciseModel.objects.filter(mentor=mentor,  student=student, is_seen_by_mentor=False)
        num_exercises_viewed = exercises_viewed.count()
        num_exercises_not_viewed = exercises_not_viewed.count()
        return Response({'num_exercises_viewed': num_exercises_viewed, 'num_exercises_not_viewed': num_exercises_not_viewed})
    


class StudentPanelSendExercise(APIView):

#   authentication_classes = [JWTAuthentication]


    def post(self,request, *args, **kwargs):
      
        student = Student.objects.get(user=request.user)

        serializer = StudentExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(student=student)
        instance.is_done_exercise = True
        instance.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetPostedExerciseOfStudent(APIView):
   #   authentication_classes = [JWTAuthentication]



    def get(self, request, *args, **kwargs):
  
        student = Student.objects.get(user=request.user)
        exercises_done = StudentExerciseModel.objects.filter(student=student)
       
        serializer = StudentExerciseSerializer(instance=exercises_done, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetStudentExerciseStatus(APIView):
#   authentication_classes = [JWTAuthentication]
 
    def get(self, request, *args, **kwargs):

        student = Student.objects.get(user=request.user)
        exercises_done = StudentExerciseModel.objects.filter(student=student, is_done_exercise=True)
        exercises_not_done = StudentExerciseModel.objects.filter(student=student, is_done_exercise=False)
        num_exercises_done = exercises_done.count()
        num_exercises_not_done = exercises_not_done.count()
        return Response({'num_exercises_done': num_exercises_done, 'num_exercises_not_done': num_exercises_not_done})








#exam

class MentorCreateExam(APIView):


  #   authentication_classes = [JWTAuthentication]

    def post(self,request, *args, **kwargs):

        serializer = ExamSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor_user = request.user
        mentor = Mentor.objects.get(user=mentor_user)
        exam = serializer.save(mentor=mentor)

        # redis_client = Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
        # redis_key = exam.id
        # redis_client.set(redis_key, json.dumps(serializer.data))
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ExamStatusSendView(APIView):
#   authentication_classes = [JWTAuthentication]

    def post(self,request, *args, **kwargs):

        serializer = ExamStatusHomeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor_user = request.user
        mentor = Mentor.objects.get(user=mentor_user)
        serializer.save(mentor=mentor)
   
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ExamStatusHomeView(APIView):
   def get(self, request, *args, **kwargs):
        exercises = HomeStatusExamModel.objects.all()
    
        serializer = ExamStatusHomeSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    # def get(self, request):
    #     home_exams = HomeStatusExamModel.objects.all()
    #     exam_status_list = []

    #     for home_exam in home_exams:
    #         exam = home_exam.exam
    #         exam_status = {'exam_date': exam.exam_date, 'status': home_exam.get_status_display(), 'score': home_exam.score}
    #         exam_status_list.append(exam_status)

    #     serializer = ExamStatusHomeSerializer(exam_status_list, many=True)
    #     return Response(serializer.data)
















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