from rest_framework import serializers
from .models import FamilyGroup, Membership

# class FamilyGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FamilyGroup
#         fields = ['id', 'name', 'description', 'created_at', 'updated_at']

# class MembershipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Membership
#         fields = ['membership_id', 'family_group', 'joined_at']


# Serializer for FamilyGroup model
class FamilyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = FamilyGroup
        # Fields to be included in the serialization
        fields = '__all__'

# Serializer for Membership model
class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = Membership
        # Fields to be included in the serialization
        fields = '__all__'

