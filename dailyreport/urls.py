from django.urls import path


from .views import ReportSubmissionList, ReportSubmissionDetail
from .views import ReportListStudent, ReportDetailStudent, UnsentedReportsStudent, SentReportsStudent, SearchReportsStudent, SearchReports


urlpatterns = [
    path('reports/', ReportSubmissionList.as_view(), name='exercise_submission_list'),
    path('reports/<int:pk>/', ReportSubmissionDetail.as_view(), name='exercise_submission_detail'),
    path('reports_search/', SearchReports.as_view()),
#panel student
    path('reports-list/', ReportListStudent.as_view(), name='report-list'),
    path('reports-detail/<int:pk>/', ReportDetailStudent.as_view(), name='report-detail'),
    path('unsent-reports/', UnsentedReportsStudent.as_view(), name='unsent-reports'),
    path('sent-reports/', SentReportsStudent.as_view(), name='sent-reports'),
    path('search-reports/', SearchReportsStudent.as_view(), name='search-reports'),
]
