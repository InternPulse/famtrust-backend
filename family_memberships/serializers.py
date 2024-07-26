from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import (
    serializers,
    status,
)

from family_memberships import validators
from family_memberships.models import (
    FamilyGroup,
    FamilyMembership,
)
from famtrust import utils


class FamilyGroupSerializer(
    validators.FamilyGroupValidatorMixin, serializers.ModelSerializer
):
    """Serializer for FamilyGroup object."""

    class Meta:
        model = FamilyGroup
        fields = "__all__"
        read_only_fields = ("owner_id",)
        filterset_fields = ("is_default",)


class FamilyGroupInMembershipSerializer(serializers.ModelSerializer):
    """Serializer for FamilyGroup object in FamilyMembership."""

    class Meta:
        model = FamilyGroup
        fields = ("id", "name", "description", "is_default")


class FamilyMembershipSerializer(
    validators.FamilyMembershipValidatorMixin, serializers.ModelSerializer
):
    class Meta:
        model = FamilyMembership
        fields = "__all__"

    family_group = FamilyGroupInMembershipSerializer(read_only=True)
    family_group_id = serializers.PrimaryKeyRelatedField(
        queryset=FamilyGroup.objects.all(),
        write_only=True,
        source="family_group",
    )

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "An error occurred while creating the "
                        "family membership"
                    ),
                    "details": e.args[0],
                },
                status_code=(
                    status.HTTP_409_CONFLICT
                    if "already exists" in e.args[0]
                    else status.HTTP_400_BAD_REQUEST
                ),
            )


class FamilyMembershipInFamilyGroupSerializer(serializers.ModelSerializer):
    """Serializer for FamilyMembership object in FamilyGroup."""

    class Meta:
        model = FamilyMembership
        fields = ("id", "user_id", "joined_at")