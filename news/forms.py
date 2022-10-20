from datetime import datetime
from typing import Any, Dict

from django import forms
from django.utils.timezone import make_aware
from news.models import NewsItem


class NewsItemAPIForm(forms.ModelForm):
    """Form for processing NewsItem objects from external API."""
    
    class Meta:
        model = NewsItem
        fields = ['__all__']