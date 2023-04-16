from django.urls import path
from django.contrib.auth.views import LogoutView

from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginViewAsAdmin, MentorCreateView, StudentCreateView, CustomRedirectView, LogoutAPIView, \
    LoginViews, ApiRootView, CourseCreateView, CourseListView, CourseRetrieveUpdateDeleteView, \
    RetrieveReportView, CreateReportComment
from .authentication import ObtainTokenPairView

# from django.urls import reverse

# url = reverse('course-detail', args=[])


urlpatterns = [
    path('login/', LoginViewAsAdmin.as_view(), name='login'),
    path('roots/', ApiRootView.as_view(), name='roots'),
    path('create-mentor/', MentorCreateView.as_view(), name='create-mentor'),
    path('create-student/', StudentCreateView.as_view(), name='create-student'),
    # Course Api
    path('create-course/', CourseCreateView.as_view()),
    path('course/', CourseListView.as_view()),
    path('course/<int:pk>/', CourseRetrieveUpdateDeleteView.as_view(), name='course-detail'),

    path('api/token/', ObtainTokenPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),

    path('', CustomRedirectView.as_view()),

    # path('logout/', LogoutView.as_view(), name='logout')
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('login2/', LoginViews.as_view()),
    path('reports/', RetrieveReportView.as_view(), name='students-reports'),
    path('reports/<str:student_first_name>-<str:student_last_name>/<int:report_number>/comments/',
         CreateReportComment.as_view(), name='report-comment-create')
    # path('comment/', RetrieveReportAndCommentOnIt.as_view(), name='comment'),
]