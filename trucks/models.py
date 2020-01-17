from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from location_field.forms.plain import PlainLocationField


class Truck(models.Model):
    title = models.CharField(max_length=120, null=True)
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', null=True, blank=True, default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')
    description = models.CharField(max_length=500, null=True, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    tags = TaggableManager(verbose_name='tags', blank=True,)

    def get_short_description(self):
        return self.description[0:255] + "..."

    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    @property
    def menu(self):
        return self.menuitem_set.all()

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    price = models.FloatField(max_length=10)
    image = models.ImageField(upload_to='uploads/trucks/menu-items', null=True, blank=True)

    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)


    def __str__(self):
        return self.name
