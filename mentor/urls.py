from django.urls import path

from .views import CustomObtainAuthToken, MyTokenObtainPairView, LoginViewAsMentor, MentorDetailView

urlpatterns = [
    # path('create/', CreateMentorView.as_view(), name='create-mentor-account'),
    path('login/', LoginViewAsMentor.as_view()),
    path('detail2/<int:pk>/', MentorDetailView.as_view()),
    # path('login/', CustomObtainAuthToken.as_view())
    path('login2/', MyTokenObtainPairView.as_view())
]