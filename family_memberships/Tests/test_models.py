from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from family_memberships.models import FamilyGroup, Membership
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


class MembershipModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.family_group = FamilyGroup.objects.create(
            id=uuid.uuid4(),
            name='Test Family Group',
            description='This is a test family group.',
            owner_id=uuid.uuid4()
        )
        self.membership = Membership.objects.create(
            membership_id=uuid.uuid4(),
            user=self.user,
            family_group=self.family_group
        )

    def test_membership_creation(self):
        self.assertEqual(self.membership.user, self.user)
        self.assertEqual(self.membership.family_group, self.family_group)
        self.assertIsInstance(self.membership.joined_at, timezone.datetime)
        self.assertIsInstance(self.membership.membership_id, uuid.UUID)
    
    def test_str_method(self):
        expected_str = f"Membership {self.membership.membership_id} for {self.user} in {self.family_group}"
        self.assertEqual(str(self.membership), expected_str)
