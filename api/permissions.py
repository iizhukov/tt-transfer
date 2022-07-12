from rest_framework.permissions import BasePermission


class IsDriverUser(BasePermission):
    """
    Allows access only to drivers.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.role == "d"


class IsManagerUser(BasePermission):
    """
    Allows access only to managers.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.role == "m"
