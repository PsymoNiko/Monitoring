from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



from .models import(
     StudentExerciseModel,
     MentorExerciseModel
)

from .serializers import (
    StudentExerciseSerializer, 
    MentorExerciseSerializer,
    
)

from student.models import Student
from mentor.models import Mentor
from redis import Redis
import json

# redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
redis_client = Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

class MentorPanelSendExercise(APIView):
    # serializer_class = MentorExerciseSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return self.serializer_class(*args, **kwargs)

    # authentication_classes = [TokenAuthentication]  
    # permission_classes = [IsAuthenticated]

    # def post(self,request, *args, **kwargs):

    #     serializer = MentorExerciseSerializer(data=request.data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     mentor_user = request.user
    #     mentor = Mentor.objects.get(user=mentor_user)
    #     exercises = serializer.save(mentor=mentor)
    #     redis_key = exercises.id
    #     redis_client.set(redis_key, json.dumps(serializer.data))
        
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    



    def post(self,request, *args, **kwargs):

        serializer = MentorExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        exercises = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class GetPostedExerciseOfMentor(APIView):
    # authentication_classes = [TokenAuthentication]  
    # permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     # exercise = MentorExerciseModel.objects.all()
    #     redis_keys = redis_client.keys('exercise:*')
    #     exercises = []
    #     serializer = MentorExerciseSerializer(instance=exercises, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        exercises = MentorExerciseModel.objects.all()
    
        serializer = MentorExerciseSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







class StudentPanelSendExercise(APIView):
    # serializer_class = StudentExerciseSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return self.serializer_class(*args, **kwargs)
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]

    def post(self,request, *args, **kwargs):

        serializer = StudentExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetPostedExerciseOfStudent(APIView):
    # authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        exercises_done = StudentExerciseModel.objects.all()
        serializer = StudentExerciseSerializer(instance=exercises_done, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
