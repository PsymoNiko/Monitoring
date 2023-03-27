from django.urls import path
from .views import CreateReport

urlpatterns = [
    path('reports/', CreateReport.as_view()),
]