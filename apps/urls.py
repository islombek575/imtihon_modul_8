from django.urls import path

from apps.views import RandomQuestionListView, SendCodeAPIView, VerifyCodeAPIView

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('test/random/', RandomQuestionListView.as_view(), name='random_question'),
]
