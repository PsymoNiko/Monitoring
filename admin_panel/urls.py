from django.urls import path
from . import views
urlpatterns = [
    path("mentor/define/", views.DefineMentor.as_view(), name="define-mentor"),
    path("mentor/retrieve/", views.RetrieveMentorInfo.as_view(), name="retrieve-mentor"),
    path("mentor/update/", views.UpdateMentorInfo.as_view(), name="update-mentor"),
    path("mentor/delete/", views.DeleteMentorInfo.as_view(), name="delete-mentor"),
    path("student/define/", views.DefineStudent.as_view(), name="define-student"),
    path("student/retrieve/", views.RetrieveStudentInfo.as_view(), name="retrieve-student"),
    path("student/update/", views.UpdateStudentInfo.as_view(), name="update-student"),
    path("student/delete/", views.DeleteStudentInfo.as_view(), name="delete-student"),
    path("student/<slug:student_code>/comment/", views.CommentOnReport.as_view(), name="comment-on-student-report")
]


