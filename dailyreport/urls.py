from django.urls import path


from .views import ReportListStudent, ReportDetailStudent, UnsentedReportsStudent, SentReportsStudent, SearchReportsStudent
from .views import MentorReportSubmissionSearch,MentorReportSubmissionList,MentorReportSubmissionDetail


urlpatterns = [
    path('reports/', MentorReportSubmissionList.as_view(), name='report_submission_list'),
    path('reports/<int:pk>/', MentorReportSubmissionDetail.as_view(), name='report_submission_detail'),
    path('search/', MentorReportSubmissionSearch.as_view(), name='report_submission_search'),

#panel student
    path('reports-list/', ReportListStudent.as_view(), name='report-list'),
    path('reports-detail/<int:pk>/', ReportDetailStudent.as_view(), name='report-detail'),
    path('unsent-reports/', UnsentedReportsStudent.as_view(), name='unsent-reports'),
    path('sent-reports/', SentReportsStudent.as_view(), name='sent-reports'),
    path('search-reports/', SearchReportsStudent.as_view(), name='search-reports'),
]
