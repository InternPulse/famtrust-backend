from django.test import TestCase
from ..models import FamilyGroup, Membership
from rest_framework.exceptions import ValidationError
import uuid

# Create your tests here.


class FamilyGroupModelTest(TestCase):

    def test_create_family_group(self):
        """Tests creating a FamilyGroup object with valid data."""
        name = "Test Family Group"
        description = "This is a test description."
        family_group = FamilyGroup.objects.create(name=name, description=description)
        self.assertEqual(family_group.name, name)
        self.assertEqual(family_group.description, description)
        self.assertIsInstance(family_group.id, uuid.UUID)
        self.assertIsNotNone(family_group.created_at)


    def test_create_family_group_without_description(self):
        """Tests creating a FamilyGroup object without a description."""
        name = "Test Family Group"
        family_group = FamilyGroup.objects.create(name=name)
        self.assertEqual(family_group.name, name)
        self.assertEqual(family_group.description, "")

    def test_invalid_name(self):
        """Tests creating a FamilyGroup object with an empty name."""
        with self.assertRaises(ValidationError):
            FamilyGroup.objects.create(name="")





class MembershipModelTest(TestCase):

    def setUp(self):
        self.family_group = FamilyGroup.objects.create(name="Test Family Group")

    def test_create_membership(self):
        """Tests creating a Membership object with valid data."""
        member_name = "John Doe"
        email = "johndoe@example.com"
        membership = Membership.objects.create(
            family_group=self.family_group, member_name=member_name, email=email
        )
        self.assertEqual(membership.family_group, self.family_group)
        self.assertEqual(membership.member_name, member_name)
        self.assertEqual(membership.email, email)
        self.assertIsInstance(membership.id, uuid.UUID)
        self.assertIsNotNone(membership.joined_at)
        self.assertEqual(membership.role, "member")  # Default role

    def test_create_membership_with_admin_role(self):
        """Tests creating a Membership object with an admin role."""
        member_name = "Jane Doe"
        email = "janedoe@example.com"
        membership = Membership.objects.create(
            family_group=self.family_group,
            member_name=member_name,
            email=email,
            role="admin",
        )
        self.assertEqual(membership.role, "admin")

    def test_invalid_email(self):
        """Tests creating a Membership object with an invalid email."""
        member_name = "John Doe"
        email = "invalid_email"
        with self.assertRaises(ValidationError):
            Membership.objects.create(
                family_group=self.family_group, member_name=member_name, email=email
            )



