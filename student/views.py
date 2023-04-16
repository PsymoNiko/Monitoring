import redis

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login

from .models import Student, Payment, Report
# from ceo.models import Admin
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer,\
    LoginViewAsStudentSerializer, ReportSerializer#, PaymentSerializer

from django.shortcuts import redirect
from rest_framework.authtoken.models import Token


# class CreateStudentView(APIView):
#     @method_decorator(login_required)
#     def post(self, request):
#         # Check if the user is an admin
#         if not request.user.is_staff:
#             return Response({'error': 'You do not have permission to create a student account.'},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         # Get the request data and create the new student account
#         try:
#             admin = Admin.objects.get(user=request.user)
#             student_firstname = request.data['first_name']
#             student_lastname = request.data['last_name']
#             student_phone_number = request.data['phone_number']
#             student_birthday = request.data['date_of_birth']
#             student_identity_code = request.data['identity_code']
#             student_personality = request.data['personality']
#             student_avatar = request.data['avatar']
#             student = admin.create_student_account(student_firstname, student_lastname, student_phone_number,
#                                                    student_birthday, student_identity_code, student_personality,
#                                                    student_avatar)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Return the new student object
#         serializer = StudentSerializer(student)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer


class LoginViewAsStudent(generics.CreateAPIView):
    serializer_class = LoginViewAsStudentSerializer
    def create(self, request, *args, **kwargs):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in function
        student = authenticate(request, username=username, password=password)

        # Check if authentication was using
        if student is not None:
            # Log the user in using Django's built-in function
            login(request, student)
            return Response(self.get_serializer(student).data, status=status.HTTP_200_OK)

            # serializer = LoginViewAsStudentSerializer(student)
            # token, _ = Token.objects.get_or_create(user=student)

            # return redirect('detail', pk=student.pk)
            # else:
            #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            # Return a success response with the user's information
            # return Response(serializer.data, status=status.HTTP_200_OK)



        else:
            # Return an error response if authentication failed
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class StudentDetails(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = StudentSerializer(request.user, many=True, context={'request': request})
        return Response(serializer.data)


class StudentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        return Student.objects.get(user=user_id)

# {"username": "student_09109232094", "password": "0020064586"}


class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user.id)
        except Student.DoesNotExist:
            raise NotFound('Student not found')  # or return an empty queryset, depending on your desired behavior
        queryset = Report.objects.filter(student=student, student__user=self.request.user.id)
        return queryset

    def post(self, request, *args, **kwargs):
        # Get the student instance associated with the use
        student = Student.objects.get(user=self.request.user)
        # Create a report instance with the student field set to the student instance
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(student=student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportRetrieveView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = 'report_number'

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user.id)
        except Student.DoesNotExist:
            raise NotFound('Student not found')
        queryset = Report.objects.filter(student=student, student__user=self.request.user.id)
        return queryset


class DailyReportView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        # Get the current date and time
        current_time = timezone.now()

        # Get all students
        students = Student.objects.all()

        # Get the report numbers of all reports submitted by each student for today
        submitted_reports = Report.objects.filter(
            time_of_submit__date=current_time.date()
        ).values_list('student', 'report_number')

        # Find students who have not submitted their report for today
        missing_reports = []
        for student in students:
            # Check if the student has already submitted a report for today
            if (student.id, current_time.date().strftime('%Y%m%d')) not in submitted_reports:
                missing_reports.append(student)

        # Return the missing reports
        return missing_reports

    def post(self, request, *args, **kwargs):
        # Get the list of missing reports
        missing_reports = self.get_queryset()

        # Create a new report for each missing report
        for student in missing_reports:
            report_number = Report.objects.filter(student=student).count() + 1
            report_data = {
                'student': student.id,
                'report_text': '',
                'study_amount': 0,
                'report_number': report_number,
                'is_submitted': False,
            }
            serializer = ReportSerializer(data=report_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class ListOfUnSubmittedReportsAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user.id)
        queryset = Report.objects.filter(student=student, created_through_command=True)
        return queryset


class UpdateUnSubmittedReportAPIView(generics.UpdateAPIView):
    serializer_class = ReportSerializer
    lookup_field = 'report_number'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user.id)
        queryset = Report.objects.filter(student=student, created_through_command=True)
        return queryset


# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer





