"""The models of the project.

The model is structured into: 
    TopItem models to support Stories, Polls and Job posts.
    Comment model to hold comments,
    PollOptions to hold polls.
"""
import uuid

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ItemTypeChoices(models.TextChoices):
    """Enum of item types."""
    JOB = 'job'
    STORY = 'story'
    POLL = 'poll'
    COMMENT = 'comment'
    POLL_OPTION = 'pollopt'


class BaseItem(models.Model):
    """This is an abstract model containing common fields shared by all other models."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ext_id = models.TextField("Identifier from external API", unique=True)
    type = models.TextField(max_length=10, choices=ItemTypeChoices.choices)
    deleted = models.BooleanField(null=True, blank=True)
    by = models.TextField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    dead = models.BooleanField(null=True, blank=True)

    text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    is_local = models.BooleanField(default=False)

    class Meta:
        abstract = True
        constraints = [models.CheckConstraint(check=models.Q(type__in=ItemTypeChoices.values), name="%(class)s_check_item_type")]

    def clean(self):
        """Extends the clean method.
        
        This is done primarily to add a value for ext_id field for 
        locally generated items. 
        The ext_id of locally generated items are appended with an "L"
        to avoid any form of conflict with items coming from the external
        API.
        """
        super().clean()
        if not self.ext_id:
            self.ext_id = "".join(["L_", str(self.id)])

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class TopItem(BaseItem):
    """Model for top items (stories, polls and jobs)."""

    def __str__(self):
        return "%s: %s" % (self.type.capitalize(), self.title)


class Comment(BaseItem):
    """Model for comments."""
    parent = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'parent')

    class Meta:
        models.indexes = [models.Index(fields=["content_type", "parent"])]

    def clean(self):
        super().clean()
        self.type = ItemTypeChoices.COMMENT


class PollOption(BaseItem):
    """Model for poll options."""
    parent = models.ForeignKey(TopItem, to_field='ext_id', limit_choices_to={'type': ItemTypeChoices.POLL}, on_delete=models.CASCADE)


    def clean(self):
        super().clean()
        self.type = ItemTypeChoices.POLL_OPTION
    
