from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import StudentExerciseModel,MentorExerciseModel,ExerciseAssignment,ExerciseFile

from .serializers import (
    StudentExerciseSerializer, 
    MentorExerciseSerializer,
    ExerciseAssignmentSerializer
)

from student.models import Student
from mentor.models import Mentor

class MentorPanelGet(APIView):
    # def get(self, request, student_name):
    def get(self, request):
        try:
            student = Student.objects.get(name=last_name)
            exercise = StudentExerciseModel.objects.filter(student=student)
            mentor = MentorExerciseModel.objects.get(user=request.user)
            seen_count = exercise.filter(is_seen_by_mentor=True).count()
            unseen_count = exercise.exclude(is_seen_by_mentor=True).count()

            queryset = MentorExerciseModel.objects.all()
            serializer = MentorExerciseSerializer(instance=queryset, many=True)
            data = {
                # 'student_name': student_name,
                'seen_count': seen_count,
                'unseen_count': unseen_count,
                'exercise': serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'دانشجویی با این نام وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        

    

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
         # Get the Mentor instance corresponding to the logged-in user
        mentor = Mentor.objects.get(user=request.user)

        # mentor_exercise = serializer.save(mentor=request.user)
        mentor_exercise = serializer.save(mentor=mentor)

        send_to_all = data.get('send_to_all')
        student_name = data.get('student_name')
        exercise_file = request.FILES.get('exercise_file')
        
        if send_to_all:
            # Send exercise to all students
            students = Student.objects.all()

        elif student_name is not None:
            # Send exercise to selected students
            if len(student_name) == 0:
                return Response({'error': 'At least one student must be selected'}, status=status.HTTP_400_BAD_REQUEST)
            students = Student.objects.filter(last_name__in=student_name)

        for student in students:
            # Get the MentorExerciseModel instance for the current exercise name
            exercise_name = data.get('exercise_name')
            mentor_exercise = MentorExerciseModel.objects.get(name=exercise_name)



            exercise_assignment = ExerciseAssignment.objects.create(
                student=student,
                exercise=mentor_exercise,
                exercise_name=mentor_exercise.exercise_name # assuming the foreign key field name is "exercise_name"
            )
            # If the file was uploaded, set the exercise_file field
            if exercise_file is not None:
                exercise_assignment.exercise_file = exercise_file
                exercise_assignment.save()

        return Response({'success': True}, status=status.HTTP_200_OK)






# class studentExerciseCreate(APIView):
#     """
#     API endpoint for sending exercise answers back to the teacher
#     """
#     serializer_class = StudentExerciseSerializer

#     def get_serializer(self, *args, **kwargs):
#         return self.serializer_class(*args, **kwargs)

#     def post(self, request, format=None):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Get the student and mentor based on the names sent in the request
#         student_last_name = serializer.validated_data['student']
#         mentor_last_name = serializer.validated_data['mentor']
#         print=( mentor_last_name)

#         student = get_object_or_404(Student, last_name=student_last_name)
#         # mentor = get_object_or_404(Mentor, last_name=mentor_last_name)
#         mentor = Mentor.objects.get(user=request.user)
        


#         print=("student")
#         print=("mentor")
#         # Create a new instance of ExerciseAnswerModel with the Mentor and Student data
#         exercise_answer = StudentExerciseModel.objects.create(
#             student=student,
#             mentor=mentor,
#             # exercise=serializer.validated_data['exercise'],
#             exercise_text=serializer.validated_data['exercise_text'],
#             exercise_file=request.FILES.get('exercise_file', None),
#         )

#         return Response({'success': True}, status=status.HTTP_201_CREATED)




class studentExerciseCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentExerciseSerializer

    
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

        serializer = StudentExerciseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
         # Get the Mentor instance corresponding to the logged-in user
        student= Student.objects.get(user=request.user)

        # mentor_exercise = serializer.save(mentor=request.user)
        student_exercise = serializer.save(student=student)

    
        mentor_name = data.get('mentor_name')
        exercise_file = request.FILES.get('exercise_file')
        
        

        if mentor_name is not None:
            # Send exercise to selected students
            if len(mentor_name) == 0:
                return Response({'error': 'At least one student must be selected'}, status=status.HTTP_400_BAD_REQUEST)
            mentor = Student.objects.filter(last_name__in=mentor_name)

        for mentor in mentor:
            # Get the MentorExerciseModel instance for the current exercise name
            exercise_name = data.get('exercise_name')
            mentor_exercise = MentorExerciseModel.objects.get(name=exercise_name)



            exercise_assignment = ExerciseAssignment.objects.create(
                student=student,
                mentor=mentor,
                # exercise_text=student_exercise_text,
                exercise=student_exercise,
                exercise_name=student_exercise.exercise_name # assuming the foreign key field name is "exercise_name"
            )
            # If the file was uploaded, set the exercise_file field
            if exercise_file is not None:
                exercise_assignment.exercise_file = exercise_file
                exercise_assignment.save()

        return Response({'success': True}, status=status.HTTP_200_OK)








# class studentExerciseCreate(APIView):
#     serializer_class = StudentExerciseSerializer

#     def get_serializer(self, *args, **kwargs):
#         return self.serializer_class(*args, **kwargs)


#     def post(self, request, format=None):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         if request.data.get('exercise_file', None) and request.data['exercise_file'].size > 10000000:
#             return Response({'error': 'نمیتوانید بیشتر از ده مگ فایل ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)

#         # Get the student and mentor based on the names sent in the request
#         student_name = request.data.get('student_name')
#         mentor_name = request.data.get('mentor_name')
        
#         student = Student.objects.get(user=request.user)

#         student = get_object_or_404(Student, last_name=student_name)
#         # student = get_object_or_404(Student, phone_number=student_name)
#         # mentor = get_object_or_404(Mentor, last_name=mentor_name)
#         mentor = Mentor.objects.get(user=request.user)
        
#         # Create a new instance of StudentExerciseModel with the Mentor and Student data
#         serializer.save(student=student, mentor=mentor)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)





class studentExerciseList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentExerciseSerializer

    def get(self, request):
        # Get the logged-in student instance
        student = Student.objects.get(user=request.user)

        # Get all ExerciseAssignments for the student
        assignments = ExerciseAssignment.objects.filter(student=student)
        # assignments = ExerciseAssignment.objects.all()

        # Serialize the ExerciseAssignments
        serializer = self.serializer_class(assignments, many=True)

        return Response(serializer.data)






class studentExerciseDetail(APIView):
    serializer_class = StudentExerciseSerializer

    def get(self, request, pk):
        exercise = StudentExerciseModel.objects.get(pk=pk)
        exercise.done_exercise += 1
        exercise.save()
        serializer = self.serializer_class(exercise)
        return Response(serializer.data)





