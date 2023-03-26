from django.urls import path

from .views import CreateMentorView, CustomObtainAuthToken, MyTokenObtainPairView

urlpatterns = [
    path('create/', CreateMentorView.as_view(), name='create-mentor-account'),
    # path('login/', CustomObtainAuthToken.as_view())
    path('login/', MyTokenObtainPairView.as_view())
]