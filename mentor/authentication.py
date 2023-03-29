from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

from .models import Mentor

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return None

        User = get_user_model()
        try:
            # user = Mentor.objects.get(user=username)
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return (user, token.key)
        except Mentor.DoesNotExist:
            raise Warning('Invalid username/password')