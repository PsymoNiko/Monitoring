from django.urls import path
from . import views


urlpatterns = [
    path('reports/', views.DailyReportView.as_view()),
    path('reports/unsubmitted/', views.UnsubmittedReportsView.as_view()),
    path('reports/delayed/', views.DelayedReportsView.as_view()),
    path('reports/summery/', views.ReportSummaryView.as_view()),
]