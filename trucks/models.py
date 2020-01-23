from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from location_field.forms.plain import PlainLocationField

WEEKDAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]


class Truck(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', null=True, blank=True,
                              default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')
    description = models.CharField(max_length=500, null=True, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = TaggableManager(verbose_name='tags', blank=True)

    def get_short_description(self):
        return self.description[0:255] + "..."

    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    @property
    def hours_of_operation(self):
        return self.hours.all()

    @property
    def menu(self):
        return self.items.all()

    def __str__(self):
        return self.title


@receiver(post_save, sender=Truck)
def create_times(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 8):
            OpenningTime.objects.create(truck=instance, weekday=i)


class OpenningTime(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='hours')
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(default='09:00')
    to_hour = models.TimeField(default='17:00')

    class Meta:
        unique_together = ('truck', 'weekday',)

    def __str__(self):
        return WEEKDAYS[self.weekday - 1][1]


class MenuItem(models.Model):
    TYPE_ENTRE = 1
    TYPE_SIDE = 2
    TYPE_DRINK = 3
    TYPE_DESERT = 4
    TYPE_COMBO = 5

    TYPE_CHOICES = [
        (TYPE_ENTRE, 'Entre'),
        (TYPE_SIDE, 'Side'),
        (TYPE_DRINK, 'Drink'),
        (TYPE_DESERT, 'Desert')
    ]

    type = models.IntegerField(choices=TYPE_CHOICES)

    # non-specific
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=120, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    price = models.FloatField(max_length=10)
    image = models.ImageField(upload_to='uploads/trucks/menu-items', null=True, blank=True)
    
    # specific
    
    # TODO: #
    # add other types #
    # query choices by current truck field #
    entre = models.ForeignKey('self', on_delete=models.CASCADE, limit_choices_to={'type': 1,}, null=True, blank=True)



    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    def __str__(self):
        return self.name

