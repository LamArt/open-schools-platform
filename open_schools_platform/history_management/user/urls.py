from django.urls import path

from open_schools_platform.history_management.user.views import HistoryApi

urlpatterns = [
    path('<uuid:pk>', HistoryApi.as_view(), name='user_history')
]
