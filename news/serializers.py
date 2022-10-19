from rest_framework import serializers

from .models import TopItem


class TopItemSerializer(serializes.ModelSerializer):
  """Serializer for local API endpoint for adding news items."""
  model = TopItem
  exclude = ['id', 'ext_id']
