from rest_framework import serializers
from .models import FamilyGroup, Membership

# Serializer for FamilyGroup model
class FamilyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyGroup
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'owner_id']

# Serializer for Membership model
class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['membership_id', 'user_id', 'family_group', 'joined_at']
