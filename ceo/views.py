from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.reverse import reverse

import mentor.models
from mentor.serializers import MentorSerializer
from mentor.models import Mentor
from student.models import Student, AdminPayment
from student.serializers import StudentSerializer
from .serializers import LoginViewAsAdminSerializer, CourseSerializers, DailyNoteSerializers, AdminPaymentSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.views import LogoutView

from .models import Course, DailyNote


class LoginViewAsAdmin(generics.CreateAPIView):
    serializer_class = LoginViewAsAdminSerializer

    def create(self, request, *args, **kwargs):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            # serializer = LoginViewAsAdminSerializer(user)
            return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

        else:

            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class ApiRootView(APIView):
    def get(self, request):
        data = {
            'roots': reverse('roots', request=request),
            'login': reverse('login', request=request),
            'mentors': reverse('create-mentor', request=request),
            'students': reverse('create-student', request=request),
            'token': reverse('token-obtain-pair', request=request),
            'refresh': reverse('refresh-token', request=request),
            'logout': reverse('logout', request=request),
        }

        return Response(data)


class MentorCreateView(generics.CreateAPIView):
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor = serializer.create(serializer.validated_data)
        # serializer.save()
        # mentor.save()

        return Response({
            'message': 'Mentor account created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Mentor.objects.all()


class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Student.objects.all()


    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        url = request_data.pop('url', None)

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if url:
            instance.url = url
            instance.save()

        return Response({
            'message': 'Student account created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class CustomRedirectView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super(CustomRedirectView, self).post(request, *args, **kwargs)
        token = response.data.get('access')
        if token:
            # Set the token in the session
            request.session['auth_token'] = token
            return HttpResponseRedirect('/ceo/roots/')  # Replace with the URL you want to redirect to
        return response

    def get_queryset(self):
        return Student.objects.all()


class LogoutAPIView(LogoutView):
    next_page = reverse_lazy('login')

    def get_redirect_url(self):
        url = self.request.GET.get('next', self.next_page)
        return url


class LoginViews(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)

            refresh = RefreshToken.for_user(user)

            request.session['access_token'] = str(refresh.access_token)

            return Response({'detail': 'Successfully logged in.'})
        else:
            return Response({'detail': 'Invalid credentials.'})


class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Course.objects.all()


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializers


class CourseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CourseSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        students = instance.mentor_of_course.all()
        student_serializer = StudentSerializer(students, many=True)
        serializer_data = serializer.data
        serializer_data['students'] = student_serializer.data
        return Response(serializer_data)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.student_course.all()
        students_serializer = StudentSerializer(queryset, many=True, context={'request': request})
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['students'] = students_serializer.data
        return Response(data)


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('course')
        return queryset


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]


class AdminDailyNotesCreation(generics.CreateAPIView):
    serializer_class = DailyNoteSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return DailyNote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyNotePagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminDailyNotesList(generics.ListAPIView):
    queryset = DailyNote.objects.order_by('-created_at')
    serializer_class = DailyNoteSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = DailyNotePagination

    # def list(self, request, *args, **kwargs):
    #     page_offset = int(request.query_params.get('page_offset', 1))
    #     if page_offset < 1:
    #         page_offset = 1
    #     self.paginator.page = page_offset
    #     paginator = Paginator(self.queryset, self.pagination_class.page_size, allow_empty_first_page=True)
    #     page = paginator.get_page(paginator.validate_number(page_offset))
    #     serializer = self.get_serializer(page, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        return DailyNote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListStudentOfEachCourse(generics.ListAPIView):
    # queryset = Course.objects.prefetch_related('student_course')
    serializer_class = CourseSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Course.objects.all()

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset.prefetch_related('student_course')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data

        for course_data in serializer_data:
            course_id = course_data['id']
            students = Student.objects.filter(course_id=course_id)
            student_serializer = StudentSerializer(students, many=True, context={'request': request})
            course_data['students'] = student_serializer.data

        return Response(serializer_data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


class AdminStudentOfEachClass(generics.RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')

        student = Student.objects.prefetch_related('course', 'user').get(pk=pk)

        # Check if the authenticated user is an admin or the student being requested
        user = self.request.user
        if not user.is_authenticated or (not user.is_staff and student.user != user):
            raise PermissionDenied("You do not have permission to perform this action.")

        return student

    # def get_object(self):
    #     user = self.request.user
    #     student = Student.objects.get(user=user)
    #
    #     return student


class PaymentCreateView(generics.CreateAPIView):
    queryset = AdminPayment.objects.all()
    serializer_class = AdminPaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
