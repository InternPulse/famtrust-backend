import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class FamilyGroup(models.Model):
    """Model for Family Group."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(null=False, blank=False, editable=False)
    updated_at = models.DateTimeField(null=False, blank=False, editable=False)
    owner_id = models.UUIDField(
        null=False,
        blank=False,
        db_index=True,
        db_comment=(
            "The ID of the user who created the family group, "
            "this person is also the owner of the family group."
        ),
    )
    is_default = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        db_comment=(
            "Indicates if the family group is the default group for "
            "the user. Only one family group can be the default group."
            "It is recommended to assign users to a default group when they "
            "first join the family."
        ),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Save the new family group and set the `created_at` and
        `updated_at` fields correctly.
        """
        if not self.created_at:
            current_time = timezone.now()
            self.created_at = current_time
            self.updated_at = current_time
        else:
            self.updated_at = timezone.now()

        return super(FamilyGroup, self).save(*args, **kwargs)

    class Meta:
        db_table = "family_groups"
        ordering = ["-created_at"]
        unique_together = ("name", "owner_id")


class FamilyMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(
        null=False,
        blank=False,
        db_comment="The ID of the user joining the family group",
    )
    family_group = models.ForeignKey(
        "FamilyGroup",
        on_delete=models.CASCADE,
        related_name="members",
    )
    joined_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = "family_memberships"
        unique_together = ("user_id", "family_group")
        ordering = ("-joined_at",)

    def __str__(self):
        return (
            f"Membership {self.id} for {self.user_id} in"
            f" {self.family_group}"
        )

    def save(self, *args, **kwargs):
        group_memberships = self.family_group.members.values_list(
            "user_id", flat=True
        )
        if self.user_id in group_memberships:
            raise ValidationError(
                _("User already exists in the family group.")
            )

        super(FamilyMembership, self).save(*args, **kwargs)