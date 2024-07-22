from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SubAccount(models.Model):
    """Model representing a SubAccount."""

    ACCOUNT_TYPE_CHOICES = [
        ("savings", "Savings Account"),
        ("investment", "Investment Account"),
    ]

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        null=False,
        default=uuid4,
        editable=False,
    )
    owner_id = models.UUIDField(
        null=False, db_comment="The user who owns this account"
    )
    created_by = models.UUIDField(
        null=False, db_comment="The user who created this account"
    )
    type = models.CharField(
        choices=ACCOUNT_TYPE_CHOICES,
        null=False,
        default="savings",
        max_length=20,
        db_comment=_("The type of account being created"),
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_index=True,
        db_comment=_("A unique name for the account"),
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        db_comment=_("Signal whether an account is active or suspended."),
    )
    balance = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        db_comment=_(
            "The balance amount of the account, this is updatable "
            "only through a transaction."
        ),
    )
    created_at = models.DateTimeField(null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(null=False, blank=False, editable=False)
    family_account = models.ForeignKey(
        to="FamilyAccount",
        null=False,
        on_delete=models.CASCADE,
        db_comment=_(
            "The family account this sub account belongs and withdraws from"
        ),
        related_name="sub_accounts",
    )

    class Meta:
        ordering = ("balance",)
        unique_together = ("family_account", "name")

    def __str__(self):
        """Return the account type and name and the current balance."""
        return f"[{self.type}]: {self.name} - {self.balance:.2f}"

    def save(self, *args, **kwargs):
        """
        Save the new SubAccount and set the `created_at` and `updated_at`
        fields correctly.
        """
        if not self.created_at:
            current_time = timezone.now()
            self.created_at = current_time
            self.updated_at = current_time
        else:
            self.updated_at = timezone.now()

        return super(SubAccount, self).save(*args, **kwargs)


class FamilyAccount(models.Model):
    """
    Model representing a Family Account, which aggregates individual
    family member sub-accounts.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    # family_group = models.ForeignKey(
    #     to="FamilyGroup",
    #     null=False,
    #     db_comment="The family group this account belongs to",
    #     on_delete=models.CASCADE,
    # )
    family_group = models.UUIDField(null=False)
    created_by = models.UUIDField(
        null=False, db_comment=_("The user who created this family account")
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(null=False, blank=False, editable=False)

    class Meta:
        ordering = ("balance",)
        unique_together = ("name", "family_group")

    def save(self, *args, **kwargs):
        """
        Save the new FamilyAccount and set the `created_at` and
        `updated_at` fields correctly.
        """
        if not self.created_at:
            current_time = timezone.now()
            self.created_at = current_time
            self.updated_at = current_time
        else:
            self.updated_at = timezone.now()

        return super(FamilyAccount, self).save(*args, **kwargs)

    def __str__(self):
        """Returns the family account name and the current balance."""
        return f"{self.name}: {self.balance}"


class FundRequest(models.Model):
    """Model for representing a account fund request."""

    REQUEST_STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("pending", "Pending"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reason = models.TextField(
        null=False,
        blank=False,
        db_comment=_("A brief explanation of why the request was made."),
    )
    requested_by = models.UUIDField(
        null=False, db_comment=_("The user who requested the funds")
    )
    family_account = models.ForeignKey(
        to="FamilyAccount",
        null=True,
        on_delete=models.CASCADE,
        db_comment=_("The family account to request from."),
        related_name="fund_requests",
    )
    source_account = models.ForeignKey(
        to="SubAccount",
        null=False,
        on_delete=models.CASCADE,
        db_comment=_("The account to be funded if the request is accepted"),
    )
    request_status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS_CHOICES,
        default="pending",
        null=False,
        blank=False,
        db_comment=_(
            "The status of the fund request. The pending is default.\n"
            "Only an admin or authorized user can reject or accept a fund "
            "request.\n"
            "The requester can cancel the fund request, which eventually "
            "cancels the fund request."
        ),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        db_comment=_("The amount " "requested for the fund request."),
    )
    created_at = models.DateTimeField(null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(null=False, blank=False, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """
        Save the new fund request and set the `created_at` and
        `updated_at` fields correctly.
        """
        if not self.created_at:
            current_time = timezone.now()
            self.created_at = current_time
            self.updated_at = current_time
        else:
            self.updated_at = timezone.now()

        return super(FundRequest, self).save(*args, **kwargs)

    def __str__(self):
        """A string representation of the fund request."""
        return (
            f"Request ID: {self.id}:\n"
            f"\tRequester ID: {self.requested_by}\n"
            f"\tReason: {self.reason}"
        )
