from typing import Any, Dict, Optional, Type

from django.db import models
from django.forms import BaseForm
from django.shortcuts import render
from django.views import generic

from .forms import FeedUserForm
from .models import FeedUser


class CreateFeedUserView(generic.CreateView):
    """Create a feed user."""

    form_class: Optional[Type[BaseForm]] = FeedUserForm
    template_name: str = "feeduser/new.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = FeedUserForm(initial={"is_local": True})
        return context


class FeedUserDetailView(generic.DetailView):
    """View details of a FeedUser object."""

    model: Type[models.Model] = FeedUser
