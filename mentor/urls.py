from django.urls import path

from .views import CustomObtainAuthToken, MyTokenObtainPairView, LoginViewAsMentor, MentorDetailView, RetrieveReports, \
    CreateReportComment

urlpatterns = [
    # path('create/', CreateMentorView.as_view(), name='create-mentor-account'),
    path('login/', LoginViewAsMentor.as_view()),
    path('detail2/<int:pk>/', MentorDetailView.as_view()),
    # path('login/', CustomObtainAuthToken.as_view())
    path('login2/', MyTokenObtainPairView.as_view()),
    path('reports/', RetrieveReports.as_view(), name='students-reports'),
    path('reports/<str:student_first_name>-<str:student_last_name>/<int:report_number>/comments/',
         CreateReportComment.as_view(), name='report-comment-create'),
    # path('comment/on/', MentorCommentOnReportCreateAPIView.as_view(), name='comment')
]