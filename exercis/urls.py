from django.urls import path
from .views import studentExerciseCreate, studentExerciseDetail, studentExerciseList, MentorPanel


urlpatterns = [
    path('exercises/', studentExerciseCreate.as_view(), name='exercises_create'),
    path('exercises/list/', studentExerciseList.as_view(), name='exercises_list'),
    path('exercises/<int:pk>/', studentExerciseDetail.as_view(), name='exercises_detail'),
    path('exercises/mentor/', MentorPanel.as_view(), name='exercises_mentor'),


]