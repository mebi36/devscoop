from typing import Any, Dict
from django.shortcuts import render
from django.views import generic
from rest_framework import generics 

from .serializers import TopItemSerializer
from .models import TopItem, ItemTypeChoices

class LatestTopItemListView(generic.ListView):
    """Display latest news items."""
    model = TopItem
    paginate_by: int = 20


    def get_queryset(self):
        qs = TopItem.objects.all().order_by('-time')
        if "item_type" in self.kwargs:
            qs.filter(type=self.kwargs["item_type"])
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["item_types"] = [ItemTypeChoices.JOB, ItemTypeChoices.POLL, ItemTypeChoices.STORY]
        return context

    
class  TopItemApiListCreateView(generics.ListCreateView):
  """API view to enable addition of news items locally."""
    queryset = TopItem.objects.all()
    serializer = TopItemSerializer


class HomeView(generic.TemplateView):
    """Home view of the application."""
    template_name: str = "home.html"
