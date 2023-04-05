# from django.urls import path
# from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
#
from .views import StudentTokenObtainPairSerializer, LoginViewAsStudent, StudentDetails, StudentDetailView, \
    ReportRetrieveAPIView
#
# urlpatterns = [
#     path('reports/', views.DailyReportView.as_view()),
#     path('reports/unsubmitted/', views.UnsubmittedReportsView.as_view()),
#     path('reports/delayed/', views.DelayedReportsView.as_view()),
#     path('reports/summery/', views.ReportSummaryView.as_view()),
#     path('login2/', TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
#     path('login/', LoginViewAsStudent.as_view()),
#     path('detail/', StudentDetails.as_view()),
#     path('detail2/<int:pk>/', StudentDetailView.as_view()),
# ]
from django.urls import path, include
from rest_framework import routers
from .views import StudentViewSet, ReportListCreateView

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('login2/', TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
    path('login/', LoginViewAsStudent.as_view()),
    path('detail/', StudentDetails.as_view()),
    path('detail2/<int:pk>/', StudentDetailView.as_view()),
    path('reports/', ReportListCreateView.as_view(), name='report_list_create'),
    # path('student/reports/<str:report_number>/', ReportRetrieveUpdateDestroyAPIView.as_view(), name='report-detail'),
    path('reports/<int:pk>/', ReportRetrieveAPIView.as_view(), name='report-detail'),
]

