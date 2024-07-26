"""
This module defines the serializers (schemas) for API requests and responses
on family groups and memberships related operations.
"""

from rest_framework import serializers
from .models import FamilyGroup, Membership


class FamilyGroupSerializer(serializers.ModelSerializer):
    """Serializer for FamilyGroup object."""

    url = serializers.HyperlinkedIdentityField(view_name="family-group-detail")

    class Meta:
        model = FamilyGroup
        fields = "__all__"


class MembershipSerializer(serializers.ModelSerializer):
    """Serializer for Membership object."""

    url = serializers.HyperlinkedIdentityField(view_name="membership-detail")
    family_group = FamilyGroupSerializer(read_only=True)
    family_group_id = serializers.PrimaryKeyRelatedField(
        queryset=FamilyGroup.objects.all(),
        write_only=True,
        source="family_group",
    )

    class Meta:
        model = Membership
        fields = "__all__"
