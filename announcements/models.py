from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=10000)

    posted_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='announcements')
    caption = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.image.name
