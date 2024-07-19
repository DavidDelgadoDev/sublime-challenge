from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from country.models import Country
from industry.models import IndustryType
from .models import Organization

# Create your tests here.
class AddOrganizationTest(APITestCase):
    def setUp(self):
        # Create initial data if needed
        Country.objects.create(name="Existing Country")
        IndustryType.objects.create(name="Existing Industry")

    def test_add_organization_success(self):
        """
        Ensure we can add a new organization.
        """
        url = reverse('add_organization')
        data = {
            "index": 1,
            "organization_id": "12345",
            "name": "New Organization",
            "website": "https://neworg.com",
            "country": "New Country",
            "description": "A new organization in the tech industry.",
            "founded": 2021,
            "industry": "New Industry",
            "number_of_employees": 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Country.objects.count(), 2)
        self.assertEqual(IndustryType.objects.count(), 2)
        self.assertEqual(Organization.objects.get().name, 'New Organization')

    def test_add_organization_invalid_data(self):
        """
        Ensure invalid data is handled correctly.
        """
        url = reverse('add_organization')
        data = {
            "organization_id": "",
            "name": "",
            "website": "not a url",
            "country": "",
            "description": "",
            "founded": "not a year",
            "industry": "",
            "number_of_employees": "not a number"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)