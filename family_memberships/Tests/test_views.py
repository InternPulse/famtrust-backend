from django.test import TestCase
from rest_framework import status
from ..views import FamilyGroup

class FamilyGroupListAPIViewTest(TestCase):

    def setUp(self):
        self.family_group_1 = FamilyGroup.objects.create(name="Test Family Group 1")
        self.family_group_2 = FamilyGroup.objects.create(name="Test Family Group 2")

    def test_get_all_family_groups(self):
        response = self.client.get('/family-groups/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_get_empty_family_groups(self):
        FamilyGroup.objects.all().delete()
        response = self.client.get('/family-groups/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertContains(response, "message': 'No family groups found")
