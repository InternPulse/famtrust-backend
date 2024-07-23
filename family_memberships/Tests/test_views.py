import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from ..models import FamilyGroup, FamilyMembership
from django.contrib.auth.models import User

class FamilyGroupViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.family_group = FamilyGroup.objects.create(
            id=uuid.uuid4(),
            name='Test Family',
            description='Test description',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            owner_id=self.user.id
        )
        self.family_group_url = '/api/v1/family-groups/'

    def test_list_family_groups(self):
        response = self.client.get(self.family_group_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_family_group(self):
        data = {
            'name': 'New Family Group',
            'description': 'Description for new family group',
            'owner_id': self.user.id
        }
        response = self.client.post(self.family_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_family_group(self):
        url = f'{self.family_group_url}{self.family_group.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_family_group(self):
        url = f'{self.family_group_url}{self.family_group.id}/'
        data = {
            'name': 'Updated Family Group',
            'description': 'Updated description'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_family_group(self):
        url = f'{self.family_group_url}{self.family_group.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class FamilyMembershipViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.family_group = FamilyGroup.objects.create(
            id=uuid.uuid4(),
            name='Test Family',
            description='Test description',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            owner_id=self.user.id
        )
        self.family_membership = FamilyMembership.objects.create(
            membership_id=uuid.uuid4(),
            user=self.user,
            family_group=self.family_group,
            joined_at=timezone.now()
        )
        self.family_membership_url = '/api/v1/family-memberships/'

    def test_list_family_memberships(self):
        response = self.client.get(self.family_membership_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_family_membership(self):
        data = {
            'user': self.user.id,
            'family_group': self.family_group.id
        }
        response = self.client.post(self.family_membership_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_family_membership(self):
        url = f'{self.family_membership_url}{self.family_membership.membership_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_family_membership(self):
        url = f'{self.family_membership_url}{self.family_membership.membership_id}/'
        data = {
            'user': self.user.id,
            'family_group': self.family_group.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_family_membership(self):
        url = f'{self.family_membership_url}{self.family_membership.membership_id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
