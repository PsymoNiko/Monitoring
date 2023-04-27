from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import StudentTokenObtainPairSerializer, LoginViewAsStudent,\
    StudentDetails, StudentDetailView, ReportListCreateView, ReportRetrieveView, ListOfUnSubmittedReportsAPIView, \
    UpdateUnSubmittedReportAPIView, ChangeStudentPasswordView,PostStudentReceiptViewSet

from rest_framework import routers

from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'student-receipt', PostStudentReceiptViewSet, basename='student-receipt')

urlpatterns = [
    # path('login/', StudentTokenObtainPairSerializer.as_view()),
    path('login2/', TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
    path('login/', LoginViewAsStudent.as_view()),
    path('detail/', StudentDetails.as_view()),
    path('detail2/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Report
    path('reports/', ReportListCreateView.as_view(), name='report-list-create'),
    path('reports/<int:report_number>/', ReportRetrieveView.as_view(), name='report-detail'),
    path('reports/unsubmitted/', ListOfUnSubmittedReportsAPIView.as_view(), name='un-submitted-list'),
    path('reports/unsubmitted/<int:report_number>/', UpdateUnSubmittedReportAPIView.as_view(), name='un-submitted'),

    # Change password
    path('change-password/', ChangeStudentPasswordView.as_view(), name='change_student_password'),
    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # path('student-receipt/', PostStudentReceiptViewSet.as_view({'post': 'list'})),
    path('', include(router.urls)),
]