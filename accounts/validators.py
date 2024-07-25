"""Validators for account related operations"""

from django.utils.translation import gettext_lazy as _
from rest_framework import (
    status,
)

from family_memberships import models as fam_models
from famtrust import utils


class FamilyAccountValidatorMixin:

    def validate(self, data):
        self._validate_user_is_admin()
        self._validate_user_is_in_default_group(data)
        self._validate_member_in_family_group(data)

        return data

    def _validate_user_is_in_default_group(self, data):
        user = self.context["request"].ft_user
        default_family = fam_models.FamilyGroup.objects.filter(
            is_default=True, members__user_id=user["id"]
        )
        if not default_family.exists():
            raise utils.HTTPException(
                detail=_("User does not have a default family group"),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    def _validate_user_is_admin(self):
        user = self.context["request"].ft_user
        if user.get("role").get("id") != "admin":
            raise utils.HTTPException(
                detail=_("Only family admins can perform this operation."),
                status_code=status.HTTP_403_FORBIDDEN,
            )

    def _validate_member_in_family_group(self, data):
        user = self.context["request"].ft_user
        try:
            family_group = fam_models.FamilyGroup.objects.get(
                id=data["family_group"].id,
            )
        except fam_models.FamilyGroup.DoesNotExist:
            raise utils.HTTPException(
                detail=_("Invalid family group"),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not family_group.members.filter(user_id=user["id"]).exists():
            raise utils.HTTPException(
                detail=_("User is not a member of the family group"),
                status_code=status.HTTP_403_FORBIDDEN,
            )
