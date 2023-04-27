from django.urls import path
from django.contrib.auth.views import LogoutView

from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginViewAsAdmin, MentorCreateView, StudentCreateView, CustomRedirectView, LogoutAPIView, \
    LoginViews, ApiRootView, CourseCreateView, CourseListView, CourseRetrieveUpdateDeleteView,\
    StudentListView, StudentDetailView, AdminDailyNotesCreation, AdminDailyNotesList,\
    ListStudentOfEachCourse, AdminStudentOfEachClass, PaymentCreateView, StudentPaymentView, \
    ChangeAdminPasswordView
from .authentication import ObtainTokenPairView

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/', LoginViewAsAdmin.as_view(), name='login'),
    path('roots/', ApiRootView.as_view(), name='roots'),
    path('create-mentor/', MentorCreateView.as_view(), name='create-mentor'),
    path('create-student/', StudentCreateView.as_view(), name='create-student'),
    # Course Api
    path('create-course/', CourseCreateView.as_view()),
    path('course/', CourseListView.as_view()),
    path('course/<int:pk>/students/', CourseRetrieveUpdateDeleteView.as_view(), name='course-detail'),

    # Home
    path('home/create-note/', AdminDailyNotesCreation.as_view()),
    path('home/notes/', AdminDailyNotesList.as_view()),

    path('api/token/', ObtainTokenPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),

    path('', CustomRedirectView.as_view()),

    # Student
    path('students/', StudentListView.as_view(), name='admin-students-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='admin-students-details'),

    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('list/', ListStudentOfEachCourse.as_view(), name='list'),
    path('list/<int:pk>/', AdminStudentOfEachClass.as_view(), name='list-student'),

    # Payment
    path('pay/', PaymentCreateView.as_view()),
    path('read-pay/<int:pk>/', StudentPaymentView.as_view()),

    # Change password
    path('change-password/', ChangeAdminPasswordView.as_view(), name='change_admin_password'),

]