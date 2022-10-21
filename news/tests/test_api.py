import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from news.models import NewsItem
from news.tests import fixtures 

class NewsItemApiListCreateViewTestCase(APITestCase):
    """Test case for NewsItemApiListCreateView."""
    def setUp(self) -> None:
        self.url = reverse("news:all-items")

    def test_news_item_list_view(self):
        """Test news item listing."""
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'count': 0, 'next': None, 'previous': None, 'results': []})
    
    def test_news_item_creation(self):
        """Test creation feature of the NewsItemApiListCreateView api point."""
        response = self.client.post(self.url, fixtures.api_story1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_populated_news_item_list_view(self):
        """Test retrieval of news item when db has news items."""
        # creation request
        create_response = self.client.post(self.url, fixtures.api_story2, format="json")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertDictContainsSubset(fixtures.api_story2, response_content["results"][0])