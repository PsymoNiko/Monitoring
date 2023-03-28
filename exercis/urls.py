from django.urls import path
from .views import StudentExerciseCreate, StudentExerciseDetail, StudentExerciseList, MentorPanel


urlpatterns = [
    path('exercises/', StudentExerciseCreate.as_view(), name='exercises_create'),
    path('exercises/list/', StudentExerciseList.as_view(), name='exercises_list'),
    path('exercises/<int:pk>/', StudentExerciseDetail.as_view(), name='exercises_detail'),
    path('exercises/mentor/', MentorPanel.as_view(), name='exercises_mentor'),


]