"""monitoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

# import requests
#
# url = "http://localhost:8000/api-auth-login/"
# data = {
#     "username": "<Your-username>", "password": "<Your-password>"
# }
#
# session = requests.Session()
# response = session.get(url)
# csrftoken = response.cookies['csrftoken']
#
# headers = {
#     "X-CSRFToken": csrftoken,
#     "Referer": url
# }
# response = session.post(url, data=data, headers=headers)
# print(response.json())

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-token-auth/', views.obtain_auth_token),

    path('ceo/', include('ceo.urls')),
    path('mentor/', include('mentor.urls')),
    path('student/', include('student.urls')),
]
