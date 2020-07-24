from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice


class Announcement(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=10000)

    posted_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('posted_on',)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Announcement)
def notify_on_announcement_creation(sender, instance, created, **kwargs):
    if created:
        devices = FCMDevice.objects.all()
        devices.send_message(data={"click_action": "FLUTTER_NOTIFICATION_CLICK", "id": "1", "status": "done", "priority": "high"},
                             title=instance.title, body=instance.description, icon="icon_notif")


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='announcements')
    caption = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.image.name
