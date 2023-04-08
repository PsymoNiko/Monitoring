from django.urls import path
from .views import studentExerciseCreate, studentExerciseDetail, studentExerciseList, MentorPanelGet, MentorPanelPost


urlpatterns = [
    #mentor
    path('exercises/send-mentor/', MentorPanelPost.as_view(), name='send_mentor'),
    path('exercises/get-mentor/', MentorPanelGet.as_view(), name='get_mentor'),

    #student
    path('exercises/send-student/', studentExerciseCreate.as_view(), name='exercises_create'),
    path('exercises/get-student/', studentExerciseList.as_view(), name='exercises_list'),
    path('exercises/<int:pk>/', studentExerciseDetail.as_view(), name='exercises_detail'),


]