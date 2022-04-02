from django.urls import path

from .views import UserApi, CreationTokenApi, VerificationApi

urlpatterns = [
    path('token', CreationTokenApi.as_view(), name='token'),
    path('token/verify', VerificationApi.as_view(), name='verification-phone-by-token'),
    path('', UserApi.as_view(), name='user'),
]

