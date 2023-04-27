from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated




from .models import(
     StudentExerciseModel,
     MentorExerciseModel,
     HomeStatusExamModel,
     Exam,
     Grade
)

from .serializers import (
    StudentExerciseSerializer, 
    MentorExerciseSerializer,
    ExamSerializer,
    ExamStatusHomeSerializer,
    GradeSerializer,
   
)
from ceo.models import Course
from student.models import Student
from mentor.models import Mentor
from redis import Redis
import json
from django.core.cache import cache

from rest_framework import generics
from django.http import Http404


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
    # def get_queryset(self):
    #     user = self.request.user
    #     if isinstance(user, Student):
    #         return Exam.objects.filter(student_name=user)
    #     elif isinstance(user, Mentor):
    #         return Exam.objects.filter(mentor=user)
    #     else:
    #         return Exam.objects.none()

    # def post(self, request, *args, **kwargs):
        # serializer = ExamSerializer(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # mentor = Mentor.objects.get(user=request.user)
        # course_name = request.data.get('course_name')
        # students = Student.objects.filter(course=course_name)

        # student_names = serializer.validated_data.pop('student_name', [])
        # send_to_all = serializer.validated_data.pop('send_to_all', False)

        # if send_to_all:
        #     students = Student.objects.all()
        #     send_to_all = True
        # else:
        #     students = student_names
        #     send_to_all = False

        # exams = []
        # for student in students:
        #     exam_number_count = Exam.objects.filter(student_name=student).count()
        #     exam = serializer.save(
        #         mentor=mentor,
        #         send_to_all=send_to_all,
        #         exam_number=exam_number_count + 1
        #     )
        #     exam.student_name.add(student)
        #     exams.append(exam)

        # response_data = serializer.to_representation(exams, many=True)
        # return Response(response_data, status=status.HTTP_201_CREATED)




















    def post(self,request, *args, **kwargs):
        serializer = ExamSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor = Mentor.objects.get(user=request.user)
        course_name = request.data.get('course_name')
        students = Student.objects.filter(course=course_name)
        exams = serializer.save(mentor=mentor)

        response_data = []
        for exam in exams:
            response_data.append(serializer.to_representation(exam))

        return Response(response_data, status=status.HTTP_201_CREATED)
    

class GetAllExam(APIView):
    def get_object(self, exam_number):
        mentor = Mentor.objects.get(user=self.request.user)
        return Exam.objects.filter(exam_number=exam_number, mentor=mentor)

    def get(self, request, exam_number, format=None):
        exams = self.get_object(exam_number)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)





class AddGradeView(APIView):
    # def get_object(self, exam_number):
    #     mentor = Mentor.objects.get(user=self.request.user)
    #     return Exam.objects.filter(exam_number=exam_number, mentor=mentor)

    # def get(self, request, exam_number, format=None):
    #     exams = self.get_object(exam_number)
    #     serializer = ExamSerializer(exams, many=True)
    #     return Response(serializer.data)
    
    def post(self, request, exam_number, student_id):
     
        exam = Exam.objects.get(exam_number=exam_number, student_name=student_id)
        student = Student.objects.get(id=student_id)
        if not exam :
            return Response({"detail": "Exam or Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        mentor = Mentor.objects.get(user=request.user)
        serializer = GradeSerializer(data=request.data, context={'request': request, 'exam': exam})
        serializer.is_valid(raise_exception=True)
        serializer.save(mentor=mentor)


        return Response(serializer.data, status=status.HTTP_201_CREATED)




class GradeListView(APIView):
    # def get(self, request):
    #     grades = Grade.objects.all()
    #     serializer = GradeSerializer(grades, many=True)
    #     return Response(serializer.data)
    def get(self, request, exam_number):
        mentor = Mentor.objects.get(user=request.user)
        exam = Exam.objects.filter(exam_number=exam_number, mentor=mentor)
        grades = Grade.objects.all()

        if exam:
            grades = Grade.objects.filter(mentor=mentor)
            serializer = GradeSerializer(grades, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



    # def get(self, request,exam_number):
    #     exam =Exam.objects.get(exam_number=exam_number)
    #     # grades = Grade.objects.all()
    #     grades = Grade.objects.filter(exam=exam)
    #     mentor = Mentor.objects.get(user=request.user)
    #     # student = Student.objects.get(id=student_name)
    #     # exam_number = Grade.objects.get(exam_number=exam_number)
    #     grades = Grade.objects.filter(mentor=mentor)
    #     serializer = GradeSerializer(grades, many=True)
    #     return Response(serializer.data)


        # mentor = Mentor.objects.get(user=request.user)
        # student = Student.objects.get(id=student_id)
        # exercises = StudentExerciseModel.objects.filter(mentor=mentor, student=student)



    # def post(self, request, pk):
    # # def post(self, request, pk, student_id):
    #     exam = Exam.objects.get(pk=pk)
    #     mentor = Mentor.objects.get(user=request.user)
    #     request.data['exam'] = exam.id
    #     # request.data['mentor'] = mentor.id
        
    #     # student = Student.objects.get(pk=request.data['student_id'])

    #     # Check if student is assigned to this exam
    #     # if student not in exam.student_name.all() and not exam.send_to_all:
    #         # return Response({'error': 'Student is not assigned to this exam.'}, status=status.HTTP_400_BAD_REQUEST)

    #     serializer = GradeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     grade = serializer.save(mentor=mentor, exam=exam)

    #     # Assign grade to student
    #     # student_grade, created = student.grade.get_or_create(exam=exam)
    #     # student_grade, created = exam.grade.get_or_create(exam=exam)
    #     student_grade, created = grade.student_name.grade.get_or_create(exam=exam)
    #     student_grade.score = grade.score
    #     student_grade.opinion = grade.opinion
    #     student_grade.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)




# class ExamDetailView(APIView):
    # serializer_class = GradeSerializer

    # def get_object(self, pk):
    #     try:
    #         return Exam.objects.get(pk=pk)
    #     except Exam.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     exam = self.get_object(pk)
    #     serializer = ExamSerializer(exam)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     exam = self.get_object(pk)
    #     serializer = GradeSerializer(exam, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data)

    # def delete(self, request, pk, format=None):
    #     exam = self.get_object(pk)
    #     exam.is_deleted = True
    #     exam.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class ExamGradeGet(APIView):
#     def get(self, request, exam_id, student_id):
#         exam, student = self.get_object(exam_id, student_id)
#         serializer = ExamSerializer(exam)
#         return Response(serializer.data)


# class ExamGradePut(APIView):
#     def put(self, request, exam_id, student_id):
#         exam, student = self.get_object(exam_id, student_id)
#         exam.score = request.data.get('score', exam.score)
#         exam.opinion = request.data.get('opinion', exam.opinion)
#         exam.save()
#         serializer = ExamSerializer(exam)
#         return Response(serializer.data)




#     def post(self, request, pk):
#         try:
#             exam = Exam.objects.get(pk=pk)
#         except Exam.DoesNotExist:
#             return Response({'detail': 'Exam with the specified pk does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         # mentor = request.user
#         # print('exam')
#         serializer = GradeSerializer(data=request.data, many=True)
#         # serializer = GradeSerializer(data=request.data, context={'exam': exam}, many=True)
#         # serializer = GradeSerializer(data=request.data, context={'exam': exam, 'mentor': mentor}, many=True)
#         serializer.is_valid(raise_exception=True)
#         grades = serializer.save(mentor=request.user)

#         # Create a new serializer instance that serializes the list of Grade objects
#         # response_serializer = GradeSerializer(grades, many=True)
#         # print(grades)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(GradeSerializer(grades, many=True).data, status=status.HTTP_201_CREATED)


# class GetAllGrade(APIView):
        
#     def get(self, request, *args, **kwargs):
        
#         student = Mentor.objects.get(user=request.user)
#         # exercises_done = StudentExerciseModel.objects.filter(student=student)
#         grads = Exam.objects.all()
#         serializer = ExamSerializer(instance=grads, many=True)
            
#         return Response(serializer.data, status=status.HTTP_200_OK)






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







class Bug(APIView):
    def get(self, request, *args, **kwargs):
        raise Http404




























































































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