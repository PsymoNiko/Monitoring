from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import StudentTokenObtainPairSerializer, LoginViewAsStudent,\
    StudentDetails, StudentDetailView, DailyReportView

urlpatterns = [
    # path('login/', StudentTokenObtainPairSerializer.as_view()),
    path('login2/', TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
    path('login/', LoginViewAsStudent.as_view()),
    path('detail/', StudentDetails.as_view()),
    path('detail2/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Report
    path('create-report/', DailyReportView.as_view()),
]