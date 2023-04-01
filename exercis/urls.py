from django.urls import path
from .views import studentExerciseCreate, studentExerciseDetail, studentExerciseList, MentorPanelGet, MentorPanelPost


urlpatterns = [
    path('exercises/', studentExerciseCreate.as_view(), name='exercises_create'),
    path('exercises/list/', studentExerciseList.as_view(), name='exercises_list'),
    path('exercises/<int:pk>/', studentExerciseDetail.as_view(), name='exercises_detail'),
    path('exercises/getmentor/', MentorPanelGet.as_view(), name='get_mentor'),
    path('exercises/sendmentor/', MentorPanelPost.as_view(), name='send_mentor'),


]