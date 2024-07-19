# Generated by Django 5.0.7 on 2024-07-19 16:32

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FamilyAccount",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("family_group", models.UUIDField()),
                (
                    "created_by",
                    models.UUIDField(
                        db_comment="The user who created this family account"
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10
                    ),
                ),
                ("created_at", models.DateTimeField(editable=False)),
                ("updated_at", models.DateTimeField(editable=False)),
            ],
            options={
                "ordering": ("balance",),
                "unique_together": {("name", "family_group")},
            },
        ),
        migrations.CreateModel(
            name="SubAccount",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "owner_id",
                    models.UUIDField(
                        db_comment="The user who owns this account"
                    ),
                ),
                (
                    "created_by",
                    models.UUIDField(
                        db_comment="The user who created this account"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("savings", "Savings Account"),
                            ("investment", "Investment Account"),
                        ],
                        db_comment="The type of account being created",
                        default="savings",
                        max_length=20,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_comment="A unique name for the account",
                        db_index=True,
                        max_length=100,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_comment="Signal whether an account is active or suspended.",
                        default=True,
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        db_comment="The balance amount of the account, this is updatable only through a transaction.",
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                    ),
                ),
                ("created_at", models.DateTimeField(editable=False)),
                ("updated_at", models.DateTimeField(editable=False)),
                (
                    "family_account",
                    models.ForeignKey(
                        db_comment="The family account this sub account belongs and withdraws from",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_accounts",
                        to="accounts_transactions.familyaccount",
                    ),
                ),
            ],
            options={
                "ordering": ("balance",),
                "unique_together": {("family_account", "name")},
            },
        ),
        migrations.CreateModel(
            name="FundRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "reason",
                    models.TextField(
                        db_comment="A brief explanation of why the request was made."
                    ),
                ),
                (
                    "requested_by",
                    models.UUIDField(
                        db_comment="The user who requested the funds"
                    ),
                ),
                (
                    "request_status",
                    models.CharField(
                        choices=[
                            ("accepted", "Accepted"),
                            ("pending", "Pending"),
                            ("rejected", "Rejected"),
                            ("cancelled", "Cancelled"),
                        ],
                        db_comment="The status of the fund request. The pending is default.\nOnly an admin or authorized user can reject or accept a fund request.\nThe requester can cancel the fund request, which eventually cancels the fund request.",
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        db_comment="The amount requested for the fund request.",
                        decimal_places=2,
                        max_digits=10,
                    ),
                ),
                ("created_at", models.DateTimeField(editable=False)),
                ("updated_at", models.DateTimeField(editable=False)),
                (
                    "family_account",
                    models.ForeignKey(
                        db_comment="The family account to request from.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fund_requests",
                        to="accounts_transactions.familyaccount",
                    ),
                ),
                (
                    "source_account",
                    models.ForeignKey(
                        db_comment="The account to be funded if the request is accepted",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts_transactions.subaccount",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
