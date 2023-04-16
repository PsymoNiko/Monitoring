from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views
from .serializers import StudentTokenObtainPairSerializer

urlpatterns = [
    path('login2/', views.TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
    path('login/', views.LoginViewAsStudent.as_view()),
    path('detail/', views.StudentDetails.as_view()),
    path('detail2/<int:pk>/', views.StudentDetailView.as_view()),
    path('reports/',views.ReportListCreateView.as_view(), name='report-list'),
    path('reports/<str:student_first_name>-<str:student_last_name>/<int:report_number>/',
         views.ReportRetrieveView.as_view(), name='report-detail'),
    path('reports/unsubmitted/', views.ListOfUnSubmittedReportsAPIView.as_view(), name='un-submitted-list'),
    path('reports/unsubmitted/<str:student_first_name>-<str:student_last_name>/<int:report_number>/',
         views.UpdateUnSubmittedReportAPIView.as_view(), name='un-submitted'),
    # path('reportcard/<int:course_id>/card/<int:year>/<int:month>/', views.ReportCardView.as_view(),
    # name='report-card'),
    path('reports/monthly/<str:student_first_name>-<str:student_last_name>/<int:year>/<int:month>/',
         views.MonthlyReportCardView.as_view(), name='monthly-report-card'),

]
