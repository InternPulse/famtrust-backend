"""Validators for account related operations"""

from django.utils.translation import gettext_lazy as _
from rest_framework import (
    status,
)

from family_memberships import models as fam_models
from famtrust import utils


class BaseValidatorMixin:
    """Base validator mixin for API operations."""

    model = None
    friendly_name = None

    def get_user(self):
        return self.context["request"].ft_user

    def __subclasscheck__(self, subclass):
        if any(not var for var in (self.model, self.friendly_name)):
            raise NotImplementedError(
                "Add the 'model' and 'friendly_name' class variables"
            )

    def validate(self, data):
        self._validate_user_is_not_frozen()
        self._validate_user_is_admin()
        self._validate_user_is_in_default_group(data)

        return data

    def _validate_user_is_not_frozen(self):
        """Validate that the user is not frozen."""
        user = self.get_user()

        if user.isFrozen:
            raise utils.HTTPException(
                detail=_("User is frozen, operation not allowed."),
                status_code=status.HTTP_403_FORBIDDEN
            )

    def _validate_user_is_in_default_group(self, data):
        """Validate that the user is in the default family group."""
        user = self.get_user()
        default_family = fam_models.FamilyGroup.objects.filter(
            is_default=True
        )
        if not default_family.filter(members__user_id=user.id):
            raise utils.HTTPException(
                detail=_("User does not belong to the default family group"),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if "owner_id" in data:
            if not default_family.filter(
                members__user_id=data["owner_id"]
            ).exists():
                raise utils.HTTPException(
                    detail=_(
                        "Owner is not a member of the default family group"
                    ),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        if "user_id" in data:
            if not default_family.filter(
                members__user_id=data["user_id"]
            ).exists():
                raise utils.HTTPException(
                    detail=_(
                        "User is not a member of the default family group"
                    ),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

    def _validate_user_is_admin(self):
        """Validate that the user is an admin."""
        user = self.get_user()
        if not user.isAdmin:
            raise utils.HTTPException(
                detail=_("Only family admins can perform this operation."),
                status_code=status.HTTP_403_FORBIDDEN,
            )
