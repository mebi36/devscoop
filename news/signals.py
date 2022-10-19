from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from . import models
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_deeduser_handler(sender, instance, created, **kwargs):
    if not created:
        return

    feed_user = models.FeedUser(user=instance, **kwargs)
    feed_user.save()