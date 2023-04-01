from django.urls import path
from django.contrib.auth.views import LogoutView

from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginViewAsAdmin, MentorCreateView, StudentCreateView, CustomRedirectView, LogoutAPIView, \
    LoginViews, ApiRootView
from .authentication import ObtainTokenPairView

urlpatterns = [
    path('login/', LoginViewAsAdmin.as_view(), name='login'),
    path('roots/', ApiRootView.as_view(), name='roots'),
    path('create-mentor/', MentorCreateView.as_view(), name='create-mentor'),
    path('create-student/', StudentCreateView.as_view(), name='create-student'),
    path('api/token/', ObtainTokenPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),

    path('', CustomRedirectView.as_view()),

    # path('logout/', LogoutView.as_view(), name='logout')
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('login2/', LoginViews.as_view())
]