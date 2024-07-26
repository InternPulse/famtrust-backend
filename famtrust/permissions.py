"""
This module defines permissions that ensure that users have the required
privileges before performing an action
"""

from rest_framework import (
    permissions,
    status,
)

from famtrust import utils


class IsAuthenticatedWithUserService(permissions.BasePermission):
    """Verify that the user is authenticated."""

    def has_permission(self, request, view):
        return hasattr(request, "ft_user")


class IsSubAccountOwnerOrCreator(permissions.BasePermission):
    """
    Verifies that the user making the change is the owner
    or creator of the account.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_id = request.ft_user.get("id")
        return user_id == obj.owner_id or user_id == obj.created_by


class IsFamilyAccountCreatorOrAdmin(permissions.BasePermission):
    """
    Verifies that the user making the change is the creator
    or an admin of the family account.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.ft_user
        user_id = user.get('id')
        if user_id != str(obj.created_by):
            raise utils.HTTPException(
                detail={
                    "error": "You are not authorized to perform this action."
                },
                status_code=status.HTTP_403_FORBIDDEN,
            )

        return True


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
