from django.urls import path

from .views import CreateMentorView

urlpatterns = [
    path('create/', CreateMentorView.as_view(), name='create-mentor-account')
]