# from django.urls import path
# from .views import index, room
#
#
# urlpatterns = [
#     path('', index, name='index'),
#     path("<str:room_name>/", room, name="room"),
# ]

from django.urls import path

from . import views
from .views import MentorshipViewSet

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('<str:room_name>/', views.room_view, name='chat-room'),
    path('chat_student/', views.MentorshipViewSet.as_view({'get': 'list'}))


]