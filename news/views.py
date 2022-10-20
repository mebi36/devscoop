from typing import Any, Dict
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from rest_framework import generics 
from rest_framework import serializers
from rest_framework.response import Response

from .serializers import TopItemCreationSerializer, TopItemSerializer
from .models import TopItem, ItemTypeChoices

class LatestTopItemListView(generic.ListView):
    """Display latest news items."""
    model = TopItem
    paginate_by: int = 20


    def get_queryset(self):
        qs = TopItem.objects.all().order_by('-time')
        # filtering by item type
        if "item_type" in self.request.GET:
            qs = qs.filter(type=self.request.GET.get("item_type"))
        # filtering by search
        if "search" in self.request.GET:
            search_txt= self.request.GET.get("search")
            qs = qs.filter(Q(title__icontains=search_txt) | Q(text__icontains=search_txt) | Q(by__icontains=search_txt))
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["item_types"] = [ItemTypeChoices.JOB, ItemTypeChoices.POLL, ItemTypeChoices.STORY]
        return context

    
class HomeView(generic.TemplateView):
    """Home view of the application."""
    template_name: str = "home.html"


# API Views
class TopItemApiListCreateView(generics.ListCreateAPIView):
    """API view to enable addition of news items locally."""
    queryset = TopItem.objects.all()
    # serializer_class = TopItemSerializer
    def get_serializer_class(self):
        if self.request.method == "POST":
            return TopItemCreationSerializer
        return TopItemSerializer

    def create(self, request, *args, **kwargs):
        """Validate local topitem creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ensure only stories, poll and jobs are being added here
        if serializer.validated_data["type"] in [ItemTypeChoices.POLL_OPTION, ItemTypeChoices.COMMENT]:
            raise serializers.ValidationError({"type":"Can only create top item (story, poll, job) posts here."})
            
        #ensure item does not exist 
        title = serializer.validated_data["title"]
        if title is not in (None, "") and TopItem.objects.filter(title__iexact=title).exists:
            raise serializers.ValidationError({"titlte": "News item with same title already exists"})


        self.perform_create(serializer)
        return Response(serializer.data)
