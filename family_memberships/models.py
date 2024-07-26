from django.db import models

# Create your models here.
from uuid import uuid4

from django.db import models
from django.utils import timezone


class FamilyGroup(models.Model):
    """
    Model representing a Family Group.
    This is the parent entity that groups various memberships together.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False, db_comment="The name of the family group")
    description = models.TextField(blank=True, null=True, db_comment="A brief description of the family group")
    created_at = models.DateTimeField(auto_now_add=True, db_comment="The date and time when the family group was created" )
    updated_at = models.DateTimeField(auto_now=True, db_comment="The date and time when the family group was last updated")

    def __str__(self):
        """Return the name of the family group."""
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'family_group'
        verbose_name = 'Family Group'
        verbose_name_plural = 'Family Groups'


class Membership(models.Model):
    """
    Model representing Membership in a Family Group.
    This links users to family groups with a specific role.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    family_group = models.ForeignKey(FamilyGroup, related_name='memberships', on_delete=models.CASCADE, db_comment="The family group this membership belongs to")
    member_name = models.CharField(max_length=255, null=False, blank=False, db_comment="The name of the member")
    email = models.EmailField(null=False, blank=False, db_comment="The email address of the member"
    )
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member')
    ]
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='member', null=False, blank=False,db_comment="The role of the member within the family group")
    joined_at = models.DateTimeField(auto_now_add=True, db_comment="The date and time when the member joined the family group"
    )

    def __str__(self):
        """Return the name of the member."""
        return self.member_name

    class Meta:
        ordering = ['family_group', 'member_name']
        db_table = 'membership'
        unique_together = ('family_group', 'email')
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
