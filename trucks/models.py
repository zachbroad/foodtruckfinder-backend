import googlemaps
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_google_maps import fields as map_fields
from phone_field import PhoneField
from taggit.managers import TaggableManager

WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
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
    address = map_fields.AddressField(max_length=200, blank=True, null=True, verbose_name='address')
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True, verbose_name='geolocation')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    tags = TaggableManager(verbose_name='tags', blank=True)
    phone = PhoneField(blank=True, help_text='Contact number')
    website = models.URLField(blank=True)

    def get_short_description(self):
        return self.description[0:255] + "..."

    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    @property
    def reviews(self):
        return self.reviews.all()

    @property
    def menus(self):
        return self.menu.all()

    @property
    def visit_history(self):
        return self.visits.all()

    @property
    def hours_of_operation(self):
        return self.hours.all()

    @property
    def reviews(self):
        return self.review.all()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        # Check if address not given when geolocation is
        if self.address == "None" or self.address is None:
            points = self.geolocation.split(',')
            lat = points[0]
            lng = points[1]
            resp = gmaps.reverse_geocode((float(lat), float(lng)))
            address_components = resp[0]['address_components']
            house_number = address_components[0]['long_name']
            street_name = address_components[1]['long_name']
            city_name = address_components[2]['long_name']
            state_abbr = address_components[4]['short_name']
            country_abbr = address_components[5]['short_name']
            self.address = "{} {}, {}, {}, {}".format(house_number, street_name, city_name, state_abbr, country_abbr)

        if self.geolocation == "None" or self.geolocation is None or self.geolocation == "":
            resp = gmaps.geocode(self.address)
            location = resp[0]['geometry']['location']
            self.geolocation = "{},{}".format(location['lat'], location['lng'])

        super().save(*args, **kwargs)


@receiver(post_save, sender=Truck)
def create_times(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 8):
            OpenningTime.objects.create(truck=instance, weekday=i)


@receiver(post_save, sender=Truck)
def create_menu(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(truck=instance, )


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
    type = models.IntegerField(choices=TYPE_CHOICES)

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


class Menu(models.Model):
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='menu')

    @property
    def combos(self):
        return self.truck.items.all().filter(type=5)

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
        (0, '0.0'),
        (1, '0.5'),
        (2, '1.0'),
        (3, '1.5'),
        (4, '2.0'),
        (5, '2.5'),
        (6, '3.0'),
        (7, '3.5'),
        (8, '4.0'),
        (9, '4.5'),
        (10, '5.0')
    ]
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='truck_rating')
    description = models.CharField(max_length=500, blank=True, null=True)
    post_created = models.DateTimeField(auto_now_add=True)
    post_edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reviewer', 'truck',)

    def __str__(self):
        return self.truck.title + ' - Review: ' + self.reviewer.username

    @property
    def all_likes(self):
        return self.likes.all().filter(is_liked=True)

    @property
    def all_dislikes(self):
        return self.likes.all().filter(is_liked=False)


class Like(models.Model):
    is_liked = models.BooleanField(null=False, blank=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_by')

    def __str__(self):
        if self.is_liked:
            liked = ' - Liked by: '
        else:
            liked = ' - Disliked by: '
        return str(self.review) + liked + str(self.liked_by)


class Visit(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='visits')
    visitor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visited = models.DateTimeField(auto_now=True)
