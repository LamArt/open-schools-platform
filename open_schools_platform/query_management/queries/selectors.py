from operator import attrgetter

from django.db.models import QuerySet
from rest_framework.exceptions import PermissionDenied

from open_schools_platform.common.selectors import selector_factory
from open_schools_platform.errors.exceptions import WrongStatusChange
from open_schools_platform.query_management.queries.filters import QueryFilter
from open_schools_platform.query_management.queries.models import Query
from open_schools_platform.user_management.users.models import User


@selector_factory(Query)
def get_query(*, filters=None, user: User = None, prefetch_related_list=None) -> Query:
    filters = filters or {}

    qs = Query.objects.all()
    query = QueryFilter(filters, qs).qs.first()

    if user and query and not user.has_perm("queries.query_access", query):
        raise PermissionDenied

    return query


def get_query_with_checks(pk: str, user: User, update_query_check: bool = False) -> Query:
    query = get_query(
        filters={"id": pk},
        user=user,
        empty_exception=True,
    )
    if update_query_check:
        if query.status != Query.Status.SENT:
            raise WrongStatusChange(f"Cant change query. It already has {query.status} status")
    return query


@selector_factory(Query)
def get_queries(*, filters=None, prefetch_related_list=None) -> QuerySet:
    filters = filters or {}

    qs = Query.objects.prefetch_related(*prefetch_related_list).all()
    queries = QueryFilter(filters, qs).qs

    return queries


def get_query_status_changes(query):
    changes = []
    if query:
        previous_status = None
        history = sorted(query.history.all(), key=attrgetter('history_date'))
        for entry in history:
            if entry.status != previous_status:
                change = {
                    "user": entry.history_user,
                    "date": entry.history_date,
                    "previous_status": previous_status,
                    "new_status": entry.status
                }
                changes.append(change)
            previous_status = entry.status
    changes.reverse()
    return changes
