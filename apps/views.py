import random
from random import randint

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Question
from apps.serializers import RandomTestModelSerializer, SendCodeSerializer, VerifyCodeSerializer
from apps.utils import send_code


class RandomQuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = RandomTestModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        all_questions = list(Question.objects.all())
        count = min(len(all_questions), 30)
        random_questions = random.sample(all_questions, count)
        return random_questions

class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = randint(100_000, 999_999)
        valid, _ttl = send_code(phone, code)
        if valid:
            return Response({'message': "sms code sent"})
        return Response({'message':f'You have {_ttl} seconds left'})

class VerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())