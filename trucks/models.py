from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from location_field.forms.plain import PlainLocationField
from phone_field import PhoneField


WEEKDAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

TYPE_ENTRE = 1
TYPE_SIDE = 2
TYPE_DRINK = 3
TYPE_DESERT = 4
TYPE_COMBO = 5

TYPE_CHOICES = [
    (TYPE_ENTRE, 'Entre'),
    (TYPE_SIDE, 'Side'),
    (TYPE_DRINK, 'Drink'),
    (TYPE_DESERT, 'Desert'),
    (TYPE_COMBO, 'Combo')
]


class Truck(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', blank=True,
                              default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')
    description = models.CharField(
        max_length=500, blank=True, default='Sorry, this truck has no description')
    location = PlainLocationField(based_fields=['city'], zoom=7, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    tags = TaggableManager(verbose_name='tags', blank=True)
    phone = PhoneField(blank=True, help_text='Contact number')
    website = models.URLField(blank=True,)
    # phone = models.Charfield   OR  phonenumber_field dep.

    def get_short_description(self):
        return self.description[0:255] + "..."

    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)
    
    @property
    def menus(self):
        return self.menu.all()

    @property
    def hours_of_operation(self):
        return self.hours.all()

    @property
    def reviews(self):
        return self.review.all()

    def __str__(self):
        return self.title


@receiver(post_save, sender=Truck)
def create_times(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 8):
            OpenningTime.objects.create(truck=instance, weekday=i)

@receiver(post_save, sender=Truck)
def create_menu(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(truck=instance,)


class OpenningTime(models.Model):
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='hours')
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(default='09:00')
    to_hour = models.TimeField(default='17:00')

    class Meta:
        unique_together = ('truck', 'weekday',)

    def __str__(self):
        return WEEKDAYS[self.weekday - 1][1]


class MenuItem(models.Model):

    type = models.IntegerField(choices=TYPE_CHOICES[0:4])

    # non-specific
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=120, null=True)
    description = models.CharField(
        max_length=500, null=True, blank=True, default='Sorry, this item has no description.')
    price = models.FloatField(max_length=10)
    image = models.ImageField(upload_to='uploads/trucks/menu-items', null=False, blank=True,
                              default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')


    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    def __str__(self):
        return self.name

    


class MenuItemCombo(models.Model):
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='combos')
    name = models.CharField(max_length=120, null=True)
    description = models.CharField(
        max_length=500, null=True, blank=True, default='Sorry, this combo has no description.')
    price = models.FloatField(max_length=10)
    image = models.ImageField(upload_to='uploads/trucks/menu-items', null=False, blank=True,
                              default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')

    entre = models.ForeignKey(MenuItem, on_delete=models.CASCADE, limit_choices_to={
                              'type': 1, }, related_name='entre')
    side1 = models.ForeignKey(MenuItem, on_delete=models.CASCADE, limit_choices_to={
                             'type': 2, }, null=True, blank=True, related_name='side1')
    side2 = models.ForeignKey(MenuItem, on_delete=models.CASCADE, limit_choices_to={
                             'type': 2, }, null=True, blank=True, related_name='side2')
    drink = models.ForeignKey(MenuItem, on_delete=models.CASCADE, limit_choices_to={
                              'type': 3, }, null=True, blank=True, related_name='drink')
    desert = models.ForeignKey(MenuItem, on_delete=models.CASCADE, limit_choices_to={
                               'type': 4, }, null=True, blank=True, related_name='desert')

    def clean_item(self):

        if self.truck != self.entre.truck:
            raise ValidationError(
                'You must set the Entre field to an entre that belongs to this truck.')
        elif self.entre == None:
            raise ValidationError(
                'You must add an Entre if you select the type combo.')

    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    def __str__(self):
        return self.name


class Menu(models.Model):
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='menu')

    @property
    def combos(self):
        return self.truck.combos.all()

    @property
    def entres(self):
        return self.truck.items.all().filter(type=1)

    @property
    def sides(self):
        return self.truck.items.all().filter(type=2)

    @property
    def drinks(self):
        return self.truck.items.all().filter(type=3)

    @property
    def deserts(self):
        return self.truck.items.all().filter(type=4)
    

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1.0'),
        (1.5, '1.5'),
        (2, '2.0'),
        (2.5, '2.5'),
        (3, '3.0'),
        (3.5, '3.5'),
        (4, '4.0'),
        (4.5, '4.5'),
        (5, '5.0')
    ]
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=RATING_CHOICES, verbose_name='rating')
    description = models.CharField(max_length=500, blank=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    post_created = models.DateTimeField(auto_now_add=True)
    post_edited = models.DateTimeField(auto_now=True)
