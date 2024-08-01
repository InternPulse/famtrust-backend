"""
This module defines the serializers (schemas) for API requests and responses
on accounts related operations.
"""
from rest_framework import (
    serializers,
)

from accounts import validators
from accounts.models import (
    FamilyAccount,
    FundRequest,
    SubAccount,
)
from family_memberships.models import FamilyGroup
from family_memberships.serializers import FamilyGroupSummarySerializer


class FundRequestInFamilyAccountSerializer(serializers.ModelSerializer):
    """Serializer for FundRequest object in FamilyAccount."""

    source_account_name = serializers.CharField(
        source="source_account.name", read_only=True
    )
    source_account_balance = serializers.DecimalField(
        source="source_account.balance",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    requested_at = serializers.DateTimeField(
        read_only=True, source="source_account.created_at"
    )

    class Meta:
        model = FundRequest
        fields = [
            "id",
            "amount",
            "request_status",
            "requested_by",
            "source_account_name",
            "source_account_balance",
            "requested_at",
        ]


class FamilyAccountSummarySerializer(serializers.ModelSerializer):
    """Serializer for FamilyAccount object in accounts summary."""

    family_group = FamilyGroupSummarySerializer(read_only=True)

    class Meta:
        model = FamilyAccount
        fields = ("id", "name", "balance", "family_group")


class SubAccountSerializer(
    validators.SubAccountValidatorMixin, serializers.ModelSerializer
):
    """Serializer for SubAccount object."""

    family_account = FamilyAccountSummarySerializer(read_only=True)
    family_account_id = serializers.PrimaryKeyRelatedField(
        queryset=FamilyAccount.objects.all(),
        write_only=True,
        source="family_account",
    )

    class Meta:
        model = SubAccount
        fields = "__all__"
        read_only_fields = ("balance", "created_by")


class SubAccountSummarySerializer(SubAccountSerializer):
    """Serializer for SubAccount object in accounts summary."""

    class Meta:
        model = SubAccount
        fields = (
            "id",
            "name",
            "owner_id",
            "type",
            "balance",
            "family_account",
        )


class SubAccountInFundRequestSerializer(SubAccountSummarySerializer):
    """Serializer for SubAccount object in FundRequest."""

    class Meta:
        model = SubAccount
        fields = ("id", "name", "balance", "type")


class FundRequestSerializer(serializers.ModelSerializer):
    """Serializer for FundRequest object."""

    source_account = SubAccountInFundRequestSerializer(read_only=True)
    source_account_id = serializers.PrimaryKeyRelatedField(
        queryset=SubAccount.objects.all(),
        write_only=True,
        source="source_account",
    )
    family_account = FamilyAccountSummarySerializer(read_only=True)
    family_account_id = serializers.PrimaryKeyRelatedField(
        queryset=FamilyAccount.objects.all(),
        write_only=True,
        source="family_account",
    )

    class Meta:
        model = FundRequest
        fields = "__all__"
        read_only_fields = ("requested_by",)


class FamilyAccountSerializer(
    validators.FamilyAccountValidatorMixin, serializers.ModelSerializer
):
    """Serializer for FamilyAccount object."""

    fund_requests = FundRequestInFamilyAccountSerializer(
        many=True, read_only=True
    )

    family_group = FamilyGroupSummarySerializer(read_only=True)
    family_group_id = serializers.PrimaryKeyRelatedField(
        source="family_group",
        write_only=True,
        queryset=FamilyGroup.objects.all(),
    )

    class Meta:
        model = FamilyAccount
        fields = "__all__"
        read_only_fields = ("balance", "created_by")
