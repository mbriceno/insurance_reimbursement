from django.http import HttpRequest
from rest_framework import permissions


class IsCustomerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view) -> bool:
        if getattr(view, "_ignore_model_permissions", False):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and request.user.role == "CUSTOMER"
        )


class IsSupport(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view) -> bool:
        return request.user.is_authenticated and request.user.role == "SUPPORT"


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view) -> bool:
        return request.user.is_authenticated and request.user.role == "ADMIN"
