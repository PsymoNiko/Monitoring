from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views
from .serializers import StudentTokenObtainPairSerializer

urlpatterns = [
    path('login2/', views.TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
    path('login/', views.LoginViewAsStudent.as_view()),
    path('detail/', views.StudentDetails.as_view()),
    path('detail2/<int:pk>/', views.StudentDetailView.as_view()),
    path('reports/', views.ReportListCreateView.as_view(), name='report-list-create'),
    path('reports/<int:report_number>/', views.ReportRetrieveView.as_view(), name='report-detail'),
]
