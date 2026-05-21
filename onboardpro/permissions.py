from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import RoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == RoleChoices.ADMIN
        )


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in (RoleChoices.HR, RoleChoices.ADMIN)
        )


class IsHROrAdmin(BasePermission):
    """HR and Admin have elevated access; Employee is restricted."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in (RoleChoices.HR, RoleChoices.ADMIN):
            return True
        if request.user.role == RoleChoices.EMPLOYEE:
            return request.method in SAFE_METHODS
        return False


class IsOwnerOrHR(BasePermission):
    """Employee may modify only own resources; HR/Admin have full access."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in (RoleChoices.HR, RoleChoices.ADMIN):
            return True
        owner = getattr(obj, 'employee', None) or getattr(obj, 'user', None)
        if owner is None and hasattr(obj, 'instance'):
            owner = obj.instance.employee
        return owner == request.user
