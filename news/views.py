from typing import Any, Dict
from django.shortcuts import render
from django.views import generic

from news.models import TopItem, ItemTypeChoices

class LatestTopItemListView(generic.ListView):
    """Display latest news items."""
    model = TopItem
    paginate_by: int = 20


    def get_queryset(self):
        return TopItem.objects.all().order_by('-time')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["item_type"] = [ItemTypeChoices.JOB, ItemTypeChoices.POLL, ItemTypeChoices.STORY]
        return context

class HomeView(generic.TemplateView):
    """Home view of the application."""
    template_name: str = "home.html"