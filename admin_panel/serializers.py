from rest_framework import serializers
from .models import DefineMentorModel, DefineStudentModel,AdminCommentAndOrganizationalCultureModel


class DefineMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefineMentorModel
        fields = "__all__"

    def validata_phone_number(self, phone_number: str) -> str:
        if len(phone_number) != 11 or 13:
            raise serializers.ValidationError("please enter a Valid Number")
        elif not phone_number.startswith("09") or str(phone_number).startswith("+989"):
            raise serializers.ValidationError("please enter a Valid Number")
        elif not phone_number[1:].isnumeric():
            raise serializers.ValidationError("please enter a Valid Number")
        return phone_number

    def validate_id_card(self, id_number: str) -> str:
        if len(id_number) != 10:
            raise serializers.ValidationError("Please Enter a Valid ID_number")
        elif not id_number.isnumeric():
            raise serializers.ValidationError("Please Enter a Valid ID_number")
        return id_number

    def validate_first_name(self, first_name: str) -> str:
        if not first_name.isalpha():
            raise serializers.ValidationError("Please Enter a Valid Name")
        return first_name

    def validate_last_name(self, last_name: str) -> str:
        if not last_name.isalpha():
            raise serializers.ValidationError("Please Enter a Valid Name")
        return last_name

    def validate_mentor_code(self, mentor_code: str) -> str:
        if not mentor_code.isnumeric():
            raise serializers.ValidationError("Please Enter a Valid Code")
        return mentor_code


class DefineStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefineStudentModel
        fields = "__all__"

    def validate_id_card(self, id_number: str) -> str:
        if len(id_number) != 10:
            raise serializers.ValidationError("Please Enter a Valid ID_number")
        elif not id_number.isnumeric():
            raise serializers.ValidationError("Please Enter a Valid ID_number")
        return id_number

    def validate_phone_number(self, phone_number: str) -> str:
        if not phone_number[1:].isnumeric():
            raise serializers.ValidationError("please enter a Valid Number")
        elif not phone_number.startswith("09") or str(phone_number).startswith("+989"):
            raise serializers.ValidationError("please enter a Valid Number")
        elif len(phone_number) != 11 or 13:
            raise serializers.ValidationError("please enter a Valid Number")
        return phone_number

    def validate_first_name(self, first_name: str) -> str:
        if not first_name.isalpha():
            raise serializers.ValidationError("Please Enter a Valid Name")
        return first_name

    def validate_last_name(self, last_name: str) -> str:
        if not last_name.isalpha():
            raise serializers.ValidationError("Please Enter a Valid Name")
        return last_name

    def validate_student_code(self, student_code: str) -> str:
        if not student_code.isnumeric():
            raise serializers.ValidationError("Please Enter a Valid Code")
        return student_code


class AdminCommentAndOrganizationalCultureSerializer(serializers.Serializer):

    class Meta:
        model = AdminCommentAndOrganizationalCultureModel
        fields = "__all__"

