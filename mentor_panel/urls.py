from django.urls import path

from .views import CustomObtainAuthToken, MyTokenObtainPairView, LoginViewAsMentor, MentorDetailView

urlpatterns = [
    path('login/', LoginViewAsMentor.as_view()),
    path('detail2/<int:pk>/', MentorDetailView.as_view()),
    path('login2/', MyTokenObtainPairView.as_view())
]
