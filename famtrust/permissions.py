"""
This module defines permissions that ensure that users have the required
privileges before performing an action.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import (
    permissions,
    status,
)

from famtrust import models, utils


class IsObjectOwnerOrCreator(permissions.BasePermission):
    """Verify that the user is the owner or creator of the object."""

    def has_object_permission(self, request, view, obj):
        """Verify the user has the required permissions."""
        if request.method in permissions.SAFE_METHODS:
            return True

        forbidden_exception = utils.HTTPException(
            detail={
                "error": _(
                    "You are not authorized to perform this action."
                )
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
        user: models.User = request.ft_user

        if hasattr(obj, "requested_by") and user.id != obj.requested_by:
            raise forbidden_exception

        if hasattr(obj, "created_by") and user.id != obj.created_by:
            raise forbidden_exception

        if hasattr(obj, "owner_id") and user.id != obj.owner_id:
            raise forbidden_exception

        return True


class IsAuthenticatedWithUserService(permissions.BasePermission):
    """Verify that the user is authenticated."""

    def has_permission(self, request, view):
        """Verify the user is authenticated."""
        return hasattr(request, "ft_user")


class IsSubAccountOwnerOrCreator(IsObjectOwnerOrCreator):
    """Verify that the user is the owner or creator of the account."""


class IsFamilyAccountCreatorOrAdmin(IsObjectOwnerOrCreator):
    """Verify that the user is the owner or an admin of the family account."""


class IsFundRequestOwnerOrCreator(IsObjectOwnerOrCreator):
    """Verify that the user is the owner or creator of the fund request."""
