"""
This module defines the models for handling transactions and related models in
the FamTrust web app.
"""

from uuid import uuid4

from django.db import models
from django.utils import timezone

from accounts import models as accounts_models
from transactions.validators import ValidateTransactionData


class TransactionDirectionEnum(models.TextChoices):
    """Enum types of transaction directions."""

    # Internal transfers
    SUB_ACCOUNT_TO_SUB_ACCOUNT = (
        "sub_account_to_sub_account",
        "Sub Account to Sub Account",
    )
    SUB_ACCOUNT_TO_FAMILY_ACCOUNT = (
        "sub_account_to_family_account",
        "Sub Account to Family Account",
    )
    FAMILY_ACCOUNT_TO_SUB_ACCOUNT = (
        "family_account_to_sub_account",
        "Family Account to Sub Account",
    )
    FAMILY_ACCOUNT_TO_FAMILY_ACCOUNT = (
        "family_account_to_family_account",
        "Family Account to Family Account",
    )

    # External transfers
    BANK_TO_SUB_ACCOUNT = "bank_to_sub_account", "Bank to Sub Account"
    SUB_ACCOUNT_TO_BANK = "sub_account_to_bank", "Sub Account to Bank"
    BANK_TO_FAMILY_ACCOUNT = (
        "bank_to_family_account",
        "Bank to Family Account",
    )
    FAMILY_ACCOUNT_TO_BANK = (
        "family_account_to_bank",
        "Family Account to Bank",
    )
    MOBILE_WALLET_TO_FAMILY_ACCOUNT = (
        "mobile_wallet_to_family_account",
        "Mobile Wallet to Family Account",
    )


class TransactionTypeEnum(models.TextChoices):
    """Enum types of transactions."""

    SAVINGS = "savings", "Savings"
    WITHDRAWAL = "withdrawal", "Withdrawal"
    INVESTMENT = "investment", "Investment"
    AIRTIME_TOP_UP = "airtime_top_up", "Airtime Top Up"
    BILL_PAYMENT = "bill_payment", "Bill Payment"
    TRANSFERS = "transfers", "Transfers"
    FUND_REQUEST = "fund_request", "Fund Request"


class TransactionStatusEnum(models.TextChoices):
    """Enum types of transaction statuses."""

    PENDING = "pending", "Pending"
    FAILED = "failed", "Failed"
    SUCCESSFUL = "successful", "Successful"
    CANCELLED = "cancelled", "Cancelled"


class Transaction(models.Model):
    """Model representing a Transaction."""

    id = models.UUIDField(
        primary_key=True, null=False, default=uuid4, editable=False
    )
    sub_source_account = models.ForeignKey(
        accounts_models.SubAccount,
        null=True,
        on_delete=models.CASCADE,
        db_comment="The source account",
        related_name="source_transactions",
    )
    sub_destination_account = models.ForeignKey(
        accounts_models.SubAccount,
        null=True,
        on_delete=models.CASCADE,
        related_name="destination_transactions",
    )
    family_source_account = models.ForeignKey(
        accounts_models.FamilyAccount,
        null=True,
        on_delete=models.CASCADE,
        db_comment="The source account",
        related_name="source_transactions",
    )
    family_destination_account = models.ForeignKey(
        accounts_models.FamilyAccount,
        null=True,
        on_delete=models.CASCADE,
        related_name="destination_transactions",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        db_comment="The transaction amount",
    )
    user_id = models.UUIDField(
        null=False, db_comment="The user who made the transaction"
    )
    transaction_type = models.CharField(
        max_length=50,
        choices=TransactionTypeEnum.choices,
        db_comment="The type of the transaction",
    )
    transaction_status = models.CharField(
        max_length=20,
        db_comment="The status of the transaction",
        choices=TransactionStatusEnum.choices,
        default=TransactionStatusEnum.PENDING,
    )
    transaction_direction = models.CharField(
        max_length=100, choices=TransactionDirectionEnum.choices
    )
    details = models.TextField(
        null=False, blank=False, db_comment="Transaction details"
    )
    fund_request_id = models.ForeignKey(
        null=True,
        to=accounts_models.FundRequest,
        on_delete=models.SET_NULL,
        db_comment="The fund request that this transaction belongs to",
    )
    created_at = models.DateTimeField(null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(null=False, blank=False, editable=False)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at", "-updated_at"]

    def save(self, *args, **kwargs):
        """
        Save the new transaction and set the `created_at` and `updated_at`
        fields correctly.
        """
        if not self.created_at:
            current_time = timezone.now()
            self.created_at = current_time
            self.updated_at = current_time
        else:
            self.updated_at = timezone.now()

        ValidateTransactionData(self)
        self.transaction_status = TransactionStatusEnum.SUCCESSFUL
        return super(Transaction, self).save(*args, **kwargs)
