from django.urls import path

from .views import(
MentorPanelSendExercise,
GetPostedExerciseOfMentor,
StudentPanelSendExercise,
GetPostedExerciseOfStudent,
MentorCreateExam,
ExamStatusSendView,
ExamStatusHomeView,
GetMentorExerciseStatus,
GetStudentExerciseStatus,
MentorStudentExerciseList,

)


urlpatterns = [
    #mentor
    path('send-exercise-mentor/', MentorPanelSendExercise.as_view(), name='send_exercise_mentor'),
    path('get-exercises-mentor/<int:student_id>/', GetPostedExerciseOfMentor.as_view(), name='get_exercise_mentor'),

    path('menotr-status/<int:student_id>/', GetMentorExerciseStatus.as_view(), name='get_status_mentor'),
    path('get-exercise-done-mentor/<int:student_id>/', MentorStudentExerciseList.as_view(), name='get_exercise_done_mentor'),
    #student
    path('send-exercise-student/', StudentPanelSendExercise.as_view(), name='exercises_create_student'),
    path('get-exercise-student/', GetPostedExerciseOfStudent.as_view(), name='exercises_list_student'),
    path('student-status/', GetStudentExerciseStatus.as_view(), name='student_status'),
   
    #exam
    path('create-exam/', MentorCreateExam.as_view()),
    path('send-status-exam/', ExamStatusSendView.as_view()),
    path('status-exam/', ExamStatusHomeView.as_view()),


]