from rest_framework import generics, serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'phone_number', 'identity_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('identity_number')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
