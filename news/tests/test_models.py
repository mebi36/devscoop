from django.db import IntegrityError
from django.test import TestCase

from news.models import NewsItem, Comment
from news.tests import fixtures


class NewsItemTestCase(TestCase):
    def setUp(self) -> None:
        self.story_obj = NewsItem.objects.create(**fixtures.story1)

    def test_successful_story_creation(self):
        story = NewsItem.objects.get(id=fixtures.story1["id"])
        self.assertEqual(story.title, fixtures.story1["title"].lower())
    
    def test_local_ext_id_generation(self):
        self.assertEqual(self.story_obj.ext_id, "".join(["L_", str(fixtures.story1["id"])]))
    
    def test_comment_creation(self):
        comment = Comment(**fixtures.story1_comment)
        self.assertEqual(comment.parent, self.story_obj.ext_id)
    
    def test_duplicate_story_title_creation(self):
        """Test duplicate story creation."""
        self.assertRaises(IntegrityError, NewsItem.objects.create, title=fixtures.story1["title"], type=fixtures.story1["type"])
    