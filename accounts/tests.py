from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework import APITestcase
from .models import Family_Account
from .models import Sub_Account
from .serializers import Family_AccountSerializer, Sub_AccountSerializer

class FamilyAccountAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.family_account = Family_Account.objects.create(name='Test Family', balance= 'Test Balance')
        self.list_url = reverse('familyaccount-list')
        self.detail_url = reverse('familyaccount-detail', kwargs={'pk': self.family_account.pk})

    def test_list_family_accounts(self):
        url = reverse('family_accounts')
        response = self.client.get(url)
        family_accounts = Family_Account.objects.all()
        serializer = Family_AccountSerializer(family_accounts, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_family_account(self):
        data = {'id': '', 'family_group_id': '',  'balance': '', 'created_at': '', 'updated_at': ''}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Family_Account.objects.count(), 2)
        self.assertEqual(Family_Account.objects.get(id=response.data['id']).name, '')

    def test_retrieve_family_account(self):
        response = self.client.get(self.detail_url)
        family_account = Family_Account.objects.get(pk=self.family_account.pk)
        serializer = Family_AccountSerializer(family_account).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_family_account(self):
        data = {'id': 'family_account', 'balance': '', 'account_name': 'savings', 'account_type': 'investment'}
        response = self.client.put(self.detail_url, data, format='json')
        self.family_account.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.family_account.name, 'Updated Family')

    def test_delete_family_account(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Family_Account.objects.count(), 0)

    def test_authentication_required(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Sub_AccountTests(APITestCase):
    def setUp(self):
        self.sub_account_data = {'id': 'Source Account', 'balance': '', 'account_name': '', 'account_type': 'Checking'}
        url = reverse('sub_accounts')
        response = self.client.get(url)
        Sub_accounts = Sub_Account.objects.all()
        serializer = Sub_AccountSerializer(Sub_accounts, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_sub_account(self):
        url = reverse('sub_account-list')
        data = {'id': 'Sub_account', 'balance': '', 'account_name': '', 'account_type': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sub_Account.objects.count(), 2)
        self.assertEqual(Sub_Account.objects.get(id=response.data['id']).name, 'New Source Account')

    def test_get_sub_accounts(self):
        url = reverse('sub_account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.sub_account.name)

    def test_update_sub_account(self):
        url = reverse('sub_account-detail', kwargs={'pk': self.sub_account.id})
        data = {'id': 'Updated Source Account', 'balance': '', 'account_name': 'savings', 'account_type': 'Investment'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sub_account.refresh_from_db()
        self.assertEqual(self.sub_account.name, 'Updated Sub Account')
        self.assertEqual(self.sub_account.balance, '')
        self.assertEqual(self.sub_account.account_type, 'Investment')

    def test_delete_sub_account(self):
        url = reverse('sub_account-detail', kwargs={'pk': self.sub_account.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sub_Account.objects.count(), 0)


