from django.urls import path
from .views import ExerciseSubmissionList, ExerciseSubmissionDetail

urlpatterns = [
    path('exercises/', ExerciseSubmissionList.as_view(), name='exercise_submission_list'),
    path('exercises/<int:pk>/', ExerciseSubmissionDetail.as_view(), name='exercise_submission_detail'),
]

#panel student
from django.urls import path
from .views import ReportList, ReportDetail, UnsentedReports, SentReports, SearchReports

urlpatterns = [
    path('reports/', ReportList.as_view(), name='report-list'),
    path('reports/<int:pk>/', ReportDetail.as_view(), name='report-detail'),
    path('unsent-reports/', UnsentedReports.as_view(), name='unsent-reports'),
    path('sent-reports/', SentReports.as_view(), name='sent-reports'),
    path('search-reports/', SearchReports.as_view(), name='search-reports'),
]
