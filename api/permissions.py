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


class IsAdminUser(BasePermission):
    """
    Allows access only to admins.
    """
    def has_permission(self, request, view) -> bool:
        return request.user.role == "a"


class IsClientUser(BasePermission):
    """
    Allows access only to clients.
    """
    def has_permission(self, request, view) -> bool:
        return request.user.role == "c"
    

class IsEmployeeUser(BasePermission):
    """
    Allows access only to employees.
    """
    def has_permission(self, request, view) -> bool:
        return request.user.role == "e"


class IsManagerOrAdminUser(BasePermission):
    """
    Allows access only to managers and admin.
    """

    def has_permission(self, request, view) -> bool:
        return bool(request.user.is_authenticated and (request.user.role in ("m", "a")))
