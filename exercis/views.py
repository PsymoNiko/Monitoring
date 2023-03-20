from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StudentExerciseModel,MentorExerciseModel
from .serializers import StudentExerciseSerializer, MentorExerciseSerializer
from student.models import Student


class studentExerciseCreate(APIView):
    def post(self, request, format=None):
        serializer = StudentExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['file'].size > 10000000:
            return Response({'error': 'نمیتوانید بیشتر از ده مگ فایل ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class studentExerciseList(APIView):
    def get(self, request, format=None):
        # exercises = StudentExerciseModel.objects.all()
        exercises = StudentExerciseSerializer.objects.filter(student__user=request.user)
        serializer = StudentExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
    

class studentExerciseDetail(APIView):
    seriallizer_class = StudentExerciseSerializer

    def get(self, request, pk):
        exercise = StudentExerciseModel.objects.get(pk=pk)
        exercise.done_exercise += 1
        exercise.save()
        serializer = self.seriallizer_class(exercise)
        return Response(serializer.data)




class MentorPanel(APIView):
    def get(self, request, student_name):
        try:
            student = Student.objects.get(name=student_name)
            exercise = StudentExerciseModel.objects.filter(student=student)
            mentor = MentorExerciseModel.objects.get(user=request.user)
            seen_count = exercise.filter(seen_by=mentor).count()
            unseen_count = exercise.exclude(seen_by=mentor).count()

            serializer = MentorExerciseSerializer(exercise, many=True)
            data = {
                'student_name': student_name,
                'seen_count': seen_count,
                'unseen_count': unseen_count,
                'exercise': serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'دانشجویی با این نام وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        # except MentorExerciseModel.DoesNotExist:
        #     return Response()
