from rest_framework.exceptions import NotFound

from open_schools_platform.user_management.users.models import User


def selector_wrapper(selector):
    def wrapper(*, filters=None, user: User = None, empty_exception: bool = False,
                empty_message: str = "There is no such object."):
        qs = selector(filters=filters, user=user)
        if empty_exception and not qs:
            raise NotFound(empty_message)
        return qs
    return wrapper