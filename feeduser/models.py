from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class FeedUser(AbstractUser):

    from_hn = models.BooleanField(default=False)
    delay = models.IntegerField(null=True, blank=True)
    karma = models.IntegerField(default=0)
    about = models.TextField(null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.from_hn is False:
            self.username = "".join(["lu_", self.username])

    def get_absolute_url(self):
        return reverse("feeduser:detail", kwargs={"pk": self.pk})
