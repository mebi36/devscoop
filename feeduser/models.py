from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class FeedUser(AbstractUser):

    is_local = models.BooleanField(default=False)
    delay = models.IntegerField(null=True, blank=True)
    karma = models.IntegerField(default=0)
    about = models.TextField(null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.is_local:
            self.username = "".join(["lu_", self.username])


    def save(self, *args, **kwargs):
        # self.clean()
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('feeduser:detail', kwargs={'pk': self.pk})