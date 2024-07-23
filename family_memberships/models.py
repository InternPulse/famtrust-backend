from django.db import models
import uuid
from django.conf import settings

class FamilyGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner_id = models.UUIDField(default=uuid.uuid4)  # Ensure this is properly set

    def __str__(self):
        return self.name

class Membership(models.Model):
    membership_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID field for primary key
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)  # Temporarily allow null
    family_group = models.ForeignKey('FamilyGroup', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Membership {self.membership_id} for {self.user} in {self.family_group}"
