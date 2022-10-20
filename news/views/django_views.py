from typing import Any, Dict
from django.views import generic
from django.db.models import Q

from news.models import NewsItem, ItemTypeChoices


class LatestNewsItemListView(generic.ListView):
    """Display latest news items."""

    model = NewsItem
    paginate_by: int = 20

    def get_queryset(self):
        qs = NewsItem.objects.all().order_by("-time")
        # filtering by item type
        if "item_type" in self.request.GET:
            qs = qs.filter(type=self.request.GET.get("item_type"))
        # filtering by search
        if "search" in self.request.GET:
            search_txt = self.request.GET.get("search")
            qs = qs.filter(
                Q(title__icontains=search_txt)
                | Q(text__icontains=search_txt)
                | Q(by__icontains=search_txt)
            )
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["item_types"] = [
            ItemTypeChoices.JOB,
            ItemTypeChoices.POLL,
            ItemTypeChoices.STORY,
        ]
        return context


class NewsItemDetailView(generic.DetailView):
    """Detail view for a news item."""

    model = NewsItem


class HomeView(generic.TemplateView):
    """Home view of the application."""

    template_name: str = "home.html"

