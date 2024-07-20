"""
This module defines permissions that ensure that users have the required
privileges before performing an action
"""

from rest_framework import permissions


class IsAuthenticatedWithUserService(permissions.BasePermission):
    """Verify that the user is authenticated."""

    def has_permission(self, request, view):
        return hasattr(request, "ft_user")


class IsAccountOwnerOrCreator(permissions.BasePermission):
    """
    Verifies that the user making the change is the owner
    or creator of the account.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_id = request.ft_user.get("id")
        return user_id == obj.owner_id or user_id == obj.created_by


class IsFundRequestOwnerOrCreator(permissions.BasePermission):
    """
    Verifies that the user making the change is the owner
    or creator of the fund request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_id = request.ft_user.get("id")
        return user_id == obj.requested_by or user_id == obj.created_by
