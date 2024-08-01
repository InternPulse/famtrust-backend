"""
Mixins to validate the data given before creating or updating a family
membership or family group.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from family_memberships import models
from famtrust import utils, validators


class FamilyGroupValidatorMixin(validators.BaseValidatorMixin):
    """Mixin to validate the data given before creating or
    updating a family group."""

    def validate(self, data):
        """Validate the data given before creating or updating a
        family group."""
        self._validate_user_is_admin()
        self._validate_default_group_exists(data)
        self._validate_unique_together(data)

        return data

    def _validate_default_group_exists(self, data):
        """Validate that only one family group can be the default group."""
        user = self.get_user()
        user_default_group = models.FamilyGroup.objects.filter(
            owner_id=user.id,
            is_default=True,
        )
        if data.get("is_default") and user_default_group.exists():
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "A default group already exists for this "
                        "user."
                    )
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        elif not user_default_group.exists() and not data.get("is_default"):
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "A default group must exist before creating a "
                        "new group."
                    )
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def _validate_unique_together(self, data):
        """Validate that the name and owner_id of the family group are
        unique together."""
        family_group = models.FamilyGroup.objects.filter(
            name=data.get("name"), owner_id=self.get_user().id
        )

        print(family_group)
        if family_group.exists():
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "A family group with the same name already "
                        "exists for this user."
                    )
                },
                status_code=status.HTTP_409_CONFLICT,
            )


class FamilyMembershipValidatorMixin(validators.BaseValidatorMixin):
    """
    Mixin to validate the data given before creating or updating a
    family membership.
    """

    def validate(self, data):
        """
        Validate the data given before creating or updating a
        family membership.
        """
        self._validate_user_is_admin()
        self._validate_user_is_in_default_group(data)
        self._validate_user_is_not_already_in_group(data)

        return data

    @staticmethod
    def _validate_user_is_not_already_in_group(data):
        """
        Validate that the user is not already a member of the family group.

        Args:
            data (dict): The data to be validated.
        """
        user_id = data.get("user_id")
        family_group = data.get("family_group")
        group_memberships = family_group.members.values_list(
            "user_id", flat=True
        )

        if user_id in group_memberships:
            raise utils.HTTPException(
                detail={"error": "User already exists in the family group."},
                status_code=status.HTTP_409_CONFLICT,
            )
