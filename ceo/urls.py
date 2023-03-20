from django.urls import path

from .views import LoginViewAsAdmin

urlpatterns = [
    path('login/', LoginViewAsAdmin.as_view(), name='login')
]