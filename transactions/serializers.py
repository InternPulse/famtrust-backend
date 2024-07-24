"""
This module defines serializers for transactions.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import (
    serializers,
    status,
)

from accounts import (
    models as accounts_models,
    serializers as accounts_serializers,
)
from famtrust import utils
from transactions import models


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""

    url = serializers.HyperlinkedIdentityField(view_name="transaction-detail")
    family_source_account = (
        accounts_serializers.FamilyAccountSummarySerializer(
            read_only=True,
        )
    )
    family_destination_account = (
        accounts_serializers.FamilyAccountSummarySerializer(
            read_only=True,
        )
    )
    family_source_account_id = serializers.PrimaryKeyRelatedField(
        queryset=accounts_models.FamilyAccount.objects.all(),
        write_only=True,
        source="family_source_account",
        required=False,
    )
    family_destination_account_id = serializers.PrimaryKeyRelatedField(
        queryset=accounts_models.FamilyAccount.objects.all(),
        write_only=True,
        source="family_destination_account",
        required=False,
    )
    sub_source_account = accounts_serializers.SubAccountSummarySerializer(
        read_only=True,
    )
    sub_destination_account = (
        accounts_serializers.SubAccountSummarySerializer(
            read_only=True,
        )
    )

    sub_source_account_id = serializers.PrimaryKeyRelatedField(
        queryset=accounts_models.SubAccount.objects.all(),
        write_only=True,
        source="sub_source_account",
        required=False,
    )
    sub_destination_account_id = serializers.PrimaryKeyRelatedField(
        queryset=accounts_models.SubAccount.objects.all(),
        write_only=True,
        source="sub_destination_account",
        required=False,
    )

    class Meta:
        model = models.Transaction
        fields = "__all__"
        read_only_fields = ("user_id", "transaction_status")

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "An error occurred while creating the transaction"
                    ),
                    "detail": _(e.args[0]),
                },
                code="error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except ValidationError as e:
            raise utils.HTTPException(
                detail={
                    "error": _(
                        "An error occurred while updating the transaction"
                    ),
                    "detail": _(e.args[0]),
                },
                code="error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
