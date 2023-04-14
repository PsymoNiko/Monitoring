
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercise/', include('exercis.urls')),
    #ali
    path('dailyreport/', include('dailyreport.urls')),
    path('api-token-auth/', views.obtain_auth_token),

    path('ceo/', include('ceo.urls')),
    path('mentor/', include('mentor.urls')),
    path('student/', include('student.urls')),

]