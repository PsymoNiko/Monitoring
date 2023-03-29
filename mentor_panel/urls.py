from django.urls import path
from . import views

urlpatterns = [
    path("comment/<slug:last_name>/", views.CommentOnReport.as_view(), name="comment-on-report")
]


from django.urls import path

from .views import CreateMentorView, CustomObtainAuthToken, MyTokenObtainPairView, LoginViewAsMentor, MentorDetailView

urlpatterns = [
    # path('create/', CreateMentorView.as_view(), name='create-mentor-account'),
    path('login/', LoginViewAsMentor.as_view()),
    path('detail2/<int:pk>/', MentorDetailView.as_view()),
    # path('login/', CustomObtainAuthToken.as_view())
    path('login2/', MyTokenObtainPairView.as_view())
]




