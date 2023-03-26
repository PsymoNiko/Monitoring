from rest_framework import serializers
from .models import MentorCommentModel


class MentorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorCommentModel
        fields = "__all__"
