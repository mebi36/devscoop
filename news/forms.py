from datetime import datetime
from typing import Any, Dict

from django import forms
from django.utils.timezone import make_aware
from news.models import TopItem


class TopItemAPIForm(forms.ModelForm):
    """Form for processing TopItem objects from external API."""
    
    class Meta:
        model = TopItem
        fields = ['__all__']