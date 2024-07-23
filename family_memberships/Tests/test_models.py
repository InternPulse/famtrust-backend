from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from family_memberships.models import FamilyGroup, FamilyMembership
import uuid

class FamilyGroupModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.family_group = FamilyGroup.objects.create(
            id=uuid.uuid4(),
            name='Test Family Group',
            description='This is a test family group.',
            owner_id=uuid.uuid4()
        )

    def test_family_group_creation(self):
        self.assertEqual(self.family_group.name, 'Test Family Group')
        self.assertEqual(self.family_group.description, 'This is a test family group.')
        self.assertIsInstance(self.family_group.created_at, timezone.datetime)
        self.assertIsInstance(self.family_group.updated_at, timezone.datetime)
        self.assertIsInstance(self.family_group.id, uuid.UUID)
        self.assertIsInstance(self.family_group.owner_id, uuid.UUID)
    
    def test_str_method(self):
        self.assertEqual(str(self.family_group), self.family_group.name)


class FamilyMembershipModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.family_group = FamilyGroup.objects.create(
            id=uuid.uuid4(),
            name='Test Family Group',
            description='This is a test family group.',
            owner_id=uuid.uuid4()
        )
        self.family_membership = FamilyMembership.objects.create(
            membership_id=uuid.uuid4(),
            user=self.user,
            family_group=self.family_group
        )

    def test_family_membership_creation(self):
        self.assertEqual(self.family_membership.user, self.user)
        self.assertEqual(self.family_membership.family_group, self.family_group)
        self.assertIsInstance(self.family_membership.joined_at, timezone.datetime)
        self.assertIsInstance(self.family_membership.membership_id, uuid.UUID)
    
    def test_str_method(self):
        expected_str = f"Family Membership {self.family_membership.membership_id} for {self.user} in {self.family_group}"
        self.assertEqual(str(self.family_membership), expected_str)
