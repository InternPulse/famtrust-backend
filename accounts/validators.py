"""Validators for the account app."""

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from accounts import models
from family_memberships import models as fam_models
from famtrust import utils
from famtrust.validators import BaseValidatorMixin


class SubAccountValidatorMixin(BaseValidatorMixin):
    """Validators for Sub Account operations."""

    model = models.SubAccount
    friendly_name = "sub account"

    def validate(self, data):
        """Validate the sub account data."""
        super().validate(data)
        self._validate_user_has_access_to_family_account(data)
        self._validate_user_does_not_have_sub_account(data)
        return data

    def _validate_user_has_access_to_family_account(self, data):
        """Validate that the user has access to the family account."""
        family_account: models.FamilyAccount = data.get("family_account")
        user = self.get_user()

        if not family_account.family_group.members.filter(
            user_id=user.id
        ).exists():
            raise utils.HTTPException(
                detail=_(
                    "User is not a member of the group this family account "
                    "is linked to"
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def _validate_user_does_not_have_sub_account(self, data):
        """
        Validate that the user does not already have a subaccount in the
        family account before creating it.

        This validation is not run when updating an instance of a subaccount.
        """
        http_method = self.get_http_method()
        user = self.get_user()
        family_account: models.FamilyAccount = data.get("family_account")

        if (
            family_account.sub_accounts.filter(owner_id=user.id).exists() and
            http_method.upper() == 'POST'
        ):
            raise utils.HTTPException(
                detail=_(
                    "User already has a sub account in this family account"
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class FamilyAccountValidatorMixin(BaseValidatorMixin):
    """Validators for Family Account operations."""

    model = models.FamilyAccount
    friendly_name = "family account"

    def validate(self, data):
        """Validate the family account data."""
        super().validate(data)
        self._validate_member_in_family_group(data)
        return data

    def _validate_member_in_family_group(self, data):
        """Validate that the user is a member of the family group."""
        user = self.context["request"].ft_user
        try:
            family_group = fam_models.FamilyGroup.objects.get(
                id=data.get("family_group").id,
            )
        except fam_models.FamilyGroup.DoesNotExist:
            raise utils.HTTPException(
                detail=_("Invalid family group"),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not family_group.members.filter(user_id=user.id).exists():
            raise utils.HTTPException(
                detail=_("User is not a member of the family group"),
                status_code=status.HTTP_403_FORBIDDEN,
            )
