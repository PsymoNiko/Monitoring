from django.urls import path
from . import views

urlpatterns = [
    path("comment/<slug:last_name>/", views.CommentOnReport.as_view(), name="comment-on-report")
]







