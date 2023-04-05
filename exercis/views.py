from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import StudentExerciseModel,MentorExerciseModel,ExerciseAssignment
from .serializers import StudentExerciseSerializer, MentorExerciseSerializer
from student.models import Student


class MentorPanelGet(APIView):
    def get(self, request, student_name):
        try:
            student = Student.objects.get(name=student_name)
            exercise = StudentExerciseModel.objects.filter(student=student)
            mentor = MentorExerciseModel.objects.get(user=request.user)
            seen_count = exercise.filter(is_seen_by_mentor=True).count()
            unseen_count = exercise.exclude(is_seen_by_mentor=True).count()

            queryset = MentorExerciseModel.objects.all()
            serializer = MentorExerciseSerializer(instance=queryset, many=True)
            data = {
                'student_name': student_name,
                'seen_count': seen_count,
                'unseen_count': unseen_count,
                'exercise': serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'دانشجویی با این نام وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        
# class MentorPanelPost(APIView):SendMentorExercise
#     serializer_class = MentorExerciseSerializer
    

#     def get_serializer(self, *args, **kwargs):
#         return self.serializer_class(*args, **kwargs)
    


class MentorPanelPost(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MentorExerciseSerializer

    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        # Convert "true" to "True" and "false" to "False"
        data = request.data.copy()
        for key in data.keys():
            if isinstance(data[key], str) and data[key].lower() == "true":
                data[key] = True
            elif isinstance(data[key], str) and data[key].lower() == "false":
                data[key] = False

        serializer = MentorExerciseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        mentor_exercise = serializer.save(mentor=request.user)

        send_to_all = data.get('send_to_all')
        student_ids = data.get('student_ids')

        if send_to_all:
            # Send exercise to all students
            students = Student.objects.all()

        elif student_ids is not None:
            # Send exercise to selected students
            if len(student_ids) == 0:
                return Response({'error': 'At least one student must be selected'}, status=status.HTTP_400_BAD_REQUEST)
            students = Student.objects.filter(id__in=student_ids)

        else:
            # Send exercise to all students
            students = Student.objects.all()

        # Create ExerciseAssignments for each student
        for student in students:
            ExerciseAssignment.objects.create(student=student, exercise=mentor_exercise)

        return Response({'success': True}, status=status.HTTP_200_OK)

    
    # def post(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     task = serializer.save()

    #     send_to_all = request.data.get('send_to_all')
    #     student_ids = request.data.get('student_ids')

    #     if send_to_all:
    #     # Send exercise to all students
    #         students = Student.objects.all()
    #         task.send_to_all = True

    #     elif student_ids:
    #     # elif student_ids is not None:
    #     # Send exercise to selected students
    #         # if len(student_ids) == 0:
    #         #     return Response({'error': 'At least one student must be selected'}, status=status.HTTP_400_BAD_REQUEST)
    #         students = Student.objects.filter(id__in=student_ids)
    #         task.send_to_all = False

    #     else:
    #         return Response({'error': '"student_ids" must be specified when "send_to_all" is not set'}, status=status.HTTP_400_BAD_REQUEST)


    #     task.send_to_all = send_to_all
    #     task.save()
    #     task.student_name.set(students)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

 

class studentExerciseCreate(APIView):
    serializer_class = StudentExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        # serializer = StudentExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if request.data['exercise_file'].size > 10000000:
        if request.data.get('exercise_file', None) and request.data['exercise_file'].size > 10000000:
            return Response({'error': 'نمیتوانید بیشتر از ده مگ فایل ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer.save(student=request.user)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class studentExerciseList(APIView):
    def get(self, request, format=None):
        exercises = StudentExerciseModel.objects.all()
        completed_exercises = StudentExerciseModel.objects.filter(student=request.user)
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





