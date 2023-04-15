from django.urls import path

from .views import(
MentorPanelSendExercise,
GetPostedExerciseOfMentor,
StudentPanelSendExercise,
GetPostedExerciseOfStudent
)


urlpatterns = [
    #mentor
    path('send-mentor/', MentorPanelSendExercise.as_view(), name='send_mentor'),
    path('get-exercises/', GetPostedExerciseOfMentor.as_view(), name='get_exercise'),
    #student
    path('send-student/', StudentPanelSendExercise.as_view(), name='exercises_create'),
    path('get-student/', GetPostedExerciseOfStudent.as_view(), name='exercises_list'),
   


]