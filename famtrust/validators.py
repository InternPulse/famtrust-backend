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

    user_not_in_group_exception = utils.HTTPException(
        detail=_("User is not in the default family group"),
        status_code=status.HTTP_400_BAD_REQUEST,
    )

    def get_user(self):
        """Get the user making the request."""
        return self.context["request"].ft_user

    def get_token(self):
        """Get the token from the request headers."""
        return self.context["request"].headers.get("Authorization")

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
        try:
            user = self.get_user()
            default_family_group = fam_models.FamilyGroup.objects.get(
                is_default=True, id=data.get("family_group").id,
                owner_id=user.id
            )
        except fam_models.FamilyGroup.DoesNotExist:
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "Default family group missing, create one and try "
                        "again."
                    )
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if "owner_id" in data and data["owner_id"] != user.id:
            user = utils.fetch_user_data(
                token=self.get_token(), user_id=data["owner_id"]
            )
            if not user:
                raise utils.HTTPException(
                    detail=_("User does not exist."),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        if "user_id" in data and data["user_id"] != user.id:
            user = utils.fetch_user_data(
                token=self.get_token(), user_id=data["user_id"]
            )
            if not user:
                raise utils.HTTPException(
                    detail=_("User does not exist."),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            if not default_family_group.filter(
                members__user_id=user.id
            ).exists():
                raise self.user_not_in_group_exception

    def _validate_user_is_admin(self):
        """Validate that the user is an admin."""
        user = self.get_user()
        if not user.isAdmin:
            raise utils.HTTPException(
                detail=_("Only family admins can perform this operation."),
                status_code=status.HTTP_403_FORBIDDEN,
            )
