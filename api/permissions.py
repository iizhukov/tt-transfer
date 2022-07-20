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


class IsManagerOrAdminUser(BasePermission):
    """
    Allows access only to managers and admin.
    """

    def has_permission(self, request, view) -> bool:
        return bool(request.user.is_authenticated and (request.user.role == "m" or request.user.role == "a"))
