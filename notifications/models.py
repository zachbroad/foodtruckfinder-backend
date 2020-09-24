from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

class Notification(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    route = models.CharField(max_length=250, null=True, blank=True)
    webview_route = models.URLField(null=True, blank=True)
    seen = models.BooleanField(null=False, blank=True, default=False)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
@receiver(post_save, sender=Notification)
def notify_on_notification_creation(sender, instance, created, **kwargs):
    if created:
        devices = FCMDevice.objects.all()
        devices.send_message(data={"click_action": "FLUTTER_NOTIFICATION_CLICK", "id": "1", "status": "done", "priority": "high", "pk": instance.pk, "route": instance.route, "webview_route": instance.webview_route, "seen": instance.seen},
                            title=instance.title, body=instance.description, icon="icon_notif")
