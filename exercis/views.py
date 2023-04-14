from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# from .models import StudentExerciseModel,MentorExerciseModel,ExerciseAssignment,ExerciseFile

from .serializers import (
    # StudentExerciseSerializer, 
    MentorExerciseSerializer,
    # ExerciseAssignmentSerializer
)

# from student.models import Student
# from mentor.models import Mentor

class MentorPanelPost(APIView):
    # serializer_class = MentorExerciseSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return self.serializer_class(*args, **kwargs)

    def post(self,request, *args, **kwargs):

        serializer = MentorExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # serializer.save(mentor=request.user)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)