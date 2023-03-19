from rest_framework import serializers
from .models import AdminCommentModel, StudentInformationModel


class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCommentModel
        fields = "__all__"


class StudentInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentInformationModel
        fields = "__all__"





