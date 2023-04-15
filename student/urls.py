from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import StudentTokenObtainPairSerializer, LoginViewAsStudent,\
    StudentDetails, StudentDetailView, ReportListCreateView, ReportRetrieveView, ListOfUnSubmittedReportsAPIView, \
    UpdateUnSubmittedReportAPIView

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

]