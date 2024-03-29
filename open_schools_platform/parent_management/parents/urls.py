from django.urls import path

from open_schools_platform.parent_management.parents.views import InviteParentQueriesListApi, \
    StudentJoinCircleQueriesListApi

urlpatterns = [
    path('/get-invitations', InviteParentQueriesListApi.as_view(), name='invite-parent-list'),
    path('/student-join-circle-queries', StudentJoinCircleQueriesListApi.as_view(),
         name='student-join-circle-queries-list'),
]
