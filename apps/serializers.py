import re
from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault, CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.models import User, Question
from apps.models.questions import Answer
from apps.utils import check_phone


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','first_name','last_name','email']

class AnswerModelSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class RandomTestModelSerializer(ModelSerializer):
    answers = AnswerModelSerializer(many=True)
    class Meta:
        model = Question
        fields = ['title','answers']

class QuestionModelSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class VerifiedUserModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = User
        exclude = ()

class SendCodeSerializer(Serializer):
    phone = CharField()

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone


class VerifyCodeSerializer(Serializer):
    code = IntegerField()
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            "data": {**tokens, **user_data}
        }
        return data

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        code = attrs.get("code")
        phone = check_phone(code=code)
        if not phone:
            raise ValidationError({'message': 'invalid or expired code'})

        self.user, _ = User.objects.get_or_create(phone=phone)
        attrs['user'] = self.user
        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
