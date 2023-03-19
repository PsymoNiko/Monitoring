from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    PERSONALITIES = (
        'INTP', 'INTJ', 'ENTJ', 'ENTP',
        'INFJ', 'INFP', 'ENFJ', 'ENFP',
        'ISTJ', 'ISFJ',' ESTJ', 'ESFJ',
        'ISTP', 'ISFP', 'ESTP', 'ESFP',
    )
    personality = serializers.ChoiceField(choices=PERSONALITIES)

    class Meta:
        model = Student
        fields = '__all__'