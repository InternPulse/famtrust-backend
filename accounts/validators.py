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
        super().validate(data)
        self._validate_user_has_access_to_family_account(data)

        return data

    def _validate_user_has_access_to_family_account(self, data):
        family_account: models.FamilyAccount = data["family_account"]
        user = self.get_user()

        if not family_account.family_group.members.filter(
            user_id=user.id
        ).exists():
            raise utils.HTTPException(
                detail=_(
                    "User is not a member of the group this family account "
                    "is linked to"
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class FamilyAccountValidatorMixin(BaseValidatorMixin):
    """Validators for Family Account operations."""

    model = models.FamilyAccount
    friendly_name = "family account"

    def validate(self, data):
        super().validate(data)
        self._validate_member_in_family_group(data)
        return data

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

        if not family_group.members.filter(user_id=user.id).exists():
            raise utils.HTTPException(
                detail=_("User is not a member of the family group"),
                status_code=status.HTTP_403_FORBIDDEN,
            )
