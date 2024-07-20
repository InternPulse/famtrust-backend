from django.db import models
import uuid

# Model for FamilyGroup
class FamilyGroup(models.Model):
    # Primary key field using UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Name of the family group
    name = models.CharField(max_length=255)
    # Optional description for the family group
    description = models.TextField(blank=True, null=True)
    # Timestamp for when the family group was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the family group was last updated
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the model
    def __str__(self):
        return self.name

# Model for Membership
class Membership(models.Model):
    # Primary key field using UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Foreign key to the FamilyGroup model
    family_group = models.ForeignKey(FamilyGroup, related_name='memberships', on_delete=models.CASCADE)
    # Name of the member
    member_name = models.CharField(max_length=255)
    # Email of the member
    email = models.EmailField()
    # Role of the member within the family group
    role = models.CharField(max_length=255, choices=[('admin', 'Admin'), ('member', 'Member')], default='member')
    # Timestamp for when the membership was created
    joined_at = models.DateTimeField(auto_now_add=True)

    # String representation of the model
    def __str__(self):
        return self.member_name




# from django.db import models
# import uuid




# class FamilyGroup(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Membership(models.Model):
#     membership_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     family_group = models.ForeignKey(FamilyGroup, related_name='memberships', on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.family_group.name} - {self.membership_id}"



