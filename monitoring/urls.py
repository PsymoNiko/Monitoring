from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)
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
    path("chat/", include("Chat.urls")),
    path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
]
