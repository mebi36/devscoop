"""The models of the project.

The model is structured into: 
    NewsItem models to support Stories, Polls and Job posts.
    Comment model to hold comments,
    PollOptions to hold polls.
"""
import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


class ItemTypeChoices(models.TextChoices):
    """Enum of item types."""

    JOB = "job"
    STORY = "story"
    POLL = "poll"
    COMMENT = "comment"
    POLL_OPTION = "pollopt"


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
    from_hn = models.BooleanField(default=False)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(type__in=ItemTypeChoices.values),
                name="%(class)s_check_item_type",
            ),
        ]

    def save(self, *args, **kwargs):
        """Extending the save method primarily to add a value to the ext_id
        field for locally generated objects.
        """
        if not self.ext_id:
            self.ext_id = "".join(["L_", str(self.id)])
        return super(BaseItem, self).save(*args, **kwargs)

    @property
    def comments(self):
        """Get comments for any kind of item.

        Comments can also have comments.
        """
        return Comment.objects.filter(parent=self.id)


class NewsItem(BaseItem):
    """Model for top items (stories, polls and jobs)."""
    class Meta:
        constraints = [models.UniqueConstraint(fields=["title"], name="%(class)s_unique_title")]

    def save(self, *args, **kwargs):
        """"Save title in lowercase to enforce UniqueConstraint on field."""
        self.title = self.title.lower()
        return super(NewsItem, self).save(*args, **kwargs)
    def __str__(self):
        return "%s: %s" % (self.type.capitalize(), self.title)

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"pk": self.id})

    def get_api_detail_url(self):
        return reverse("news:api-detail", kwargs={"pk": self.id})


class Comment(BaseItem):
    """Model for comments."""

    parent = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "parent")

    class Meta:
        models.indexes = [models.Index(fields=["content_type", "parent"])]

    def clean(self):
        super(Comment, self).clean()
        self.type = ItemTypeChoices.COMMENT


class PollOption(BaseItem):
    """Model for poll options."""

    parent = models.ForeignKey(
        NewsItem,
        to_field="ext_id",
        limit_choices_to={"type": ItemTypeChoices.POLL},
        on_delete=models.CASCADE,
    )

    def clean(self):
        super(Comment, self).clean()
        self.type = ItemTypeChoices.POLL_OPTION
