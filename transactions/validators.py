from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import transactions.models as md


class ValidateTransactionData:

    def __init__(self, transaction: md.Transaction) -> None:
        # verify that fund request id is set for fund request transactions
        if (
            transaction.transaction_type
            == md.TransactionTypeEnum.FUND_REQUEST
        ):
            self._validate_fund_request_id(transaction)

        # validate transaction direction data
        match transaction.transaction_direction:
            case md.TransactionDirectionEnum.SUB_ACCOUNT_TO_SUB_ACCOUNT:
                self._validate_sub_account_to_sub_account(transaction)
            case md.TransactionDirectionEnum.SUB_ACCOUNT_TO_FAMILY_ACCOUNT:
                self._validate_sub_account_to_family_account(transaction)
            case md.TransactionDirectionEnum.FAMILY_ACCOUNT_TO_SUB_ACCOUNT:
                self._validate_family_account_to_sub_account(transaction)
            case md.TransactionDirectionEnum.FAMILY_ACCOUNT_TO_FAMILY_ACCOUNT:
                self._validate_family_account_to_family_account(transaction)
            case md.TransactionDirectionEnum.BANK_TO_FAMILY_ACCOUNT:
                self._validate_bank_to_family_account(transaction)

    @staticmethod
    def _validate_fund_request_id(transaction: md.Transaction) -> None:
        """
        Validate that the fund request id is set for fund
        request transactions.
        """
        if not transaction.fund_request_id:
            raise ValidationError(
                _(
                    "Fund request id must be set for fund_request "
                    "transactions."
                )
            )

    @staticmethod
    def _validate_sub_account_to_sub_account(
        transaction: md.Transaction,
    ) -> None:
        """Validate sub_account_to_sub_account transaction."""
        if transaction.sub_destination_account.balance < transaction.amount:
            raise ValidationError(
                _("Not enough balance in source sub account.")
            )
        if not (
            transaction.sub_source_account
            and transaction.sub_destination_account
        ):
            raise ValidationError(
                _(
                    "Both source and destination sub accounts must be set "
                    "for sub_account_to_sub_account."
                )
            )
        if (
            transaction.sub_source_account
            == transaction.sub_destination_account_id
        ):
            raise ValidationError(
                _(
                    "Source sub account and destination sub account "
                    "cannot be the same."
                )
            )

        if (
            transaction.family_destination_account
            or transaction.family_source_account
        ):
            raise ValidationError(
                _(
                    "Family accounts cannot be set for "
                    "sub_account_to_family_account."
                )
            )

        # update the balance in the database once everything checks out well
        transaction.sub_source_account.balance -= transaction.amount
        transaction.sub_destination_account.balance += transaction.amount

        transaction.sub_source_account.save()
        transaction.sub_destination_account.save()

    @staticmethod
    def _validate_sub_account_to_family_account(
        transaction: md.Transaction,
    ) -> None:
        """Validate sub_account_to_family_account transaction."""
        if not (
            transaction.sub_source_account
            and transaction.family_destination_account_id
        ):
            raise ValidationError(
                _(
                    "Source sub account and destination family account "
                    "must be set for sub_account_to_family_account."
                )
            )

        transaction.sub_source_account.balance -= transaction.amount
        transaction.family_destination_account.balance += transaction.amount

        transaction.sub_source_account.save()
        transaction.family_destination_account.save()

    @staticmethod
    def _validate_family_account_to_sub_account(
        transaction: md.Transaction,
    ) -> None:
        """Validate family_account_to_sub_account transaction."""
        if not (
            transaction.family_source_account
            and transaction.sub_destination_account
        ):
            raise ValidationError(
                _(
                    "Source family account and destination sub account"
                    " must be set for family_account_to_sub_account."
                )
            )
        if (
            transaction.family_source_account
            == transaction.family_destination_account
        ):
            raise ValidationError(
                _(
                    "Source family account and destination family account "
                    "cannot be the same."
                )
            )
        if transaction.family_source_account.balance < transaction.amount:
            raise ValidationError(
                _("Not enough balance in source family account.")
            )

        transaction.family_source_account.balance -= transaction.amount
        transaction.sub_destination_account.balance += transaction.amount

        transaction.family_source_account.save()
        transaction.sub_destination_account.save()

    @staticmethod
    def _validate_family_account_to_family_account(
        transaction: md.Transaction,
    ) -> None:
        """Validate family_account_to_family_account transaction."""
        if transaction.family_source_account.balance < transaction.amount:
            raise ValidationError(
                _("Not enough balance in source family account.")
            )
        if not (
            transaction.family_source_account
            and transaction.family_destination_account
        ):
            raise ValidationError(
                _(
                    "Both source and destination family accounts must "
                    "be set for family_account_to_family_account."
                )
            )
        if (
            transaction.family_source_account
            == transaction.family_destination_account
        ):
            raise ValidationError(
                _(
                    "Source family account and destination family account "
                    "cannot be the same."
                )
            )

        if (
            transaction.sub_source_account
            or transaction.sub_destination_account
        ):
            raise ValidationError(
                _(
                    "Sub accounts cannot be set for "
                    "family_account_to_family_account."
                )
            )

        transaction.family_source_account.balance -= transaction.amount
        transaction.family_destination_account.balance += transaction.amount

        transaction.family_source_account.save()
        transaction.family_destination_account.save()

    @staticmethod
    def _validate_bank_to_family_account(
        transaction: md.Transaction
    ) -> None:
        """Validate bank_to_family_account transaction."""
        if not transaction.family_destination_account_id:
            raise ValidationError(
                _("Destination family account must be set.")
            )

        transaction.family_destination_account.balance += transaction.amount
        transaction.family_destination_account.save()
