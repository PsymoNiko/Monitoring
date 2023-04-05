from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (LoginViewAsAdmin, MentorCreateView, StudentCreateView,
                    CustomRedirectView, LoginViews, ApiRootView, CourseCreateView, CourseListView,
                    CourseRetrieveUpdateDeleteView,  # CreateLeaveStudent
                    )
#LogoutAPIView, \

    #SetDurationOfStudentLeave, RetrieveAndUpdateLeaveDurationLeft, CourseRetrieveUpdateDeleteView
from .authentication import ObtainTokenPairView


urlpatterns = [
    path('login/', LoginViewAsAdmin.as_view(), name='login'),
    path('roots/', ApiRootView.as_view(), name='roots'),
    path('create-mentor/', MentorCreateView.as_view(), name='create-mentor'),
    path('create-student/', StudentCreateView.as_view(), name='create-student'),
    path('create-course/', CourseCreateView.as_view()),
    path('course/', CourseListView.as_view()),
    path('course/<int:pk>/', CourseRetrieveUpdateDeleteView.as_view(), name='course-detail'),
    path('api/token/', ObtainTokenPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('', CustomRedirectView.as_view()),
    # path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('login2/', LoginViews.as_view()),
    # path('leave/', CreateLeaveStudent.as_view(), name="leave"),
    # path('set-leave-time/', SetDurationOfStudentLeave.as_view(), name="set-leave-time"),
    # path('leave_left/<int:pk>/', RetrieveAndUpdateLeaveDurationLeft.as_view(), name="leave-left")
]
