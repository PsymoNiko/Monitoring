from django.urls import path

from .views import(
MentorSendExercise,
GetPostedExerciseOfMentor,
StudentPanelSendExercise,
GetPostedExerciseOfStudent,
MentorCreateExam,
GetMentorExerciseStatus,
GetStudentExerciseStatus,
MentorStudentExerciseList,
AddGradeView,
AddGradeView,
GradeListView,
GetAllExam,
GetOnePostedExerciseOfMentor,
StudentGetExam,
ExamStatusList,
GradeView
)


urlpatterns = [
    # mentor
    path('send-exercise/<int:course_id>/', MentorSendExercise.as_view(), name='send_exercise_mentor'),
    path('get-exercises-student/<int:student_id>/', GetPostedExerciseOfMentor.as_view(), name='get_exercise_mentor'),
    path('get-exercises-student/<int:student_id>/<int:id>/', GetOnePostedExerciseOfMentor.as_view(), name='get_exercise_mentor1'),
    path('menotr-status/<int:student_id>/', GetMentorExerciseStatus.as_view(), name='get_status_mentor'),
    # get  answer
    path('get-exercise-done/<int:student_id>/', MentorStudentExerciseList.as_view(), name='get_exercise_done_mentor'),
    # student
    path('send-answer-student/<int:id>/', StudentPanelSendExercise.as_view(), name='exercises_create_student'),
    path('get-answer-student/<int:id>/', GetPostedExerciseOfStudent.as_view(), name='exercises_list_student'),
    path('student-status/', GetStudentExerciseStatus.as_view(), name='student_status'),
   
    # exam
   
    path('create-exam/<int:course_id>/', MentorCreateExam.as_view()),
    path('get-all-exam/<int:exam_id>/', GetAllExam.as_view()),

    path('exam/<int:exam_id>/<int:student_id>/', AddGradeView.as_view(), name='add_grade'),
    path('grades/<int:exam_id>/', GradeListView.as_view()),
    path('status-exam/', ExamStatusList.as_view()),
#   student
    path('send-answer-exam/<int:id>/', StudentGetExam.as_view()),
    path('grade-exam/<int:exam_id>/', GradeView.as_view()),

]