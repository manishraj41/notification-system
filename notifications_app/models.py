from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications_app.tasks import broadcast_notification

# Create your models here.
class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

#signal added for notification
@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    if created:
        print(instance.id)
        broadcast_notification(data = instance.id)