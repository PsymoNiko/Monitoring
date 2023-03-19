from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExerciseModel
from .serializers import ExerciseSerializer



class ExerciseCreate(APIView):
    def post(self, request, format=None):
        serializer = ExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['file'].size > 10000000:
            return Response({'error': 'File size should be less than 10 MB'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExerciseList(APIView):
    def get(self, request, format=None):
        exercises = ExerciseModel.objects.all()
        # exercises = ExerciseModel.objects.filter(student_id=student_id)
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
    

class ExerciseDetail(APIView):
    seriallizer_class = ExerciseSerializer

    def get(self, request, pk):
        exercise = ExerciseModel.objects.get(pk=pk)
        exercise.views += 1
        exercise.save()
        serializer = self.seriallizer_class(exercise)
        return Response(serializer.data)


