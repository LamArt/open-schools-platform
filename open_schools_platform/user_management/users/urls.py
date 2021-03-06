from django.urls import path

from .views import UserApi, CreationTokenApi, VerificationApi, CodeResendApi, RetrieveCreationTokenApi, \
    UserResetPasswordApi

urlpatterns = [
    path('token', CreationTokenApi.as_view(), name='create-token'),
    path('token/<uuid:pk>', RetrieveCreationTokenApi.as_view(), name='get-token'),
    path('token/<uuid:pk>/verify', VerificationApi.as_view(), name='verification-phone-by-token'),
    path('', UserApi.as_view(), name='user'),
    path('token/<uuid:pk>/resend', CodeResendApi.as_view(), name='resend'),
    path('reset-password', UserResetPasswordApi.as_view(), name='reset-password')
]
