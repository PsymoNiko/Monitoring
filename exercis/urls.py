from django.urls import path
from .views import ExerciseList,ExerciseCreate,ExerciseDetail


urlpatterns = [
    path('exercises/', ExerciseCreate.as_view(), name='exercises_create'),
    path('exercises/list/', ExerciseList.as_view(), name='exercises_list'),
    path('exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercises_detail'),

]