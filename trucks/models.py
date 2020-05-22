from datetime import datetime
import time
import googlemaps
from django.conf import settings
from util.time import juxtapose, datetimefield_to_datetime
from django.core import validators
from django.db import models
from django_google_maps import fields as map_fields
from phone_field import PhoneField
from rest_framework.exceptions import ValidationError




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


class Tag(models.Model):
    title = models.CharField(null=False, blank=False, unique=True, max_length=25)

    class Meta:
        ordering = [
            'title'
        ]

    def __str__(self):
        return self.title


class Truck(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', blank=True, null=False,
                              default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')
    description = models.CharField(
        max_length=500, blank=True, default='Sorry, this truck has no description')
    address = map_fields.AddressField(max_length=200, blank=True, null=True, verbose_name='address')
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True, verbose_name='geolocation')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact number')
    website = models.URLField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    @property
    def num_favorites(self):
        return self.favorites.count()

    @property
    def lat(self):
        return self.geolocation.lat

    @property
    def lng(self):
        return self.geolocation.lon

    @staticmethod
    def distance_raw(lat, lng, lat2, lng2):
        import math

        delta_lat = math.radians(lat2 - lat)
        delta_lng = math.radians(lng2 - lng)
        radius = 6371

        a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(math.radians(lat)) \
            * math.cos(math.radians(lat2)) * math.sin(delta_lng / 2) * math.sin(delta_lng / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d

    def distance(self, lat, lng):
        return Truck.distance_raw(float(lat), float(lng), float(self.geolocation.lat), float(self.geolocation.lon))

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
    def reviews(self):
        return self.review.all()

    @property
    def live(self):
        return self.live_objects.filter(current=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        g_maps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        # Check if address not given when geolocation is
        if self.address is None and self.geolocation is not None:
            points = self.geolocation.split(',')
            lat = points[0]
            lng = points[1]
            resp = g_maps.reverse_geocode((float(lat), float(lng)))
            address_components = resp[0]['address_components']
            house_number = address_components[0]['long_name']
            street_name = address_components[1]['long_name']
            city_name = address_components[2]['long_name']
            state_abbr = address_components[4]['short_name']
            country_abbr = address_components[5]['short_name']
            self.address = "{} {}, {}, {}, {}".format(house_number, street_name, city_name, state_abbr, country_abbr)

        try:
            if self.geolocation is None:
                resp = g_maps.geocode(self.address)
                location = resp[0]['geometry']['location']
                self.geolocation = "{},{}".format(location['lat'], location['lng'])
        except Exception:
            pass

        super().save(*args, **kwargs)


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
    featured = models.BooleanField(default=False)

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
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name='truck_rating',
                                 validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)])
    description = models.CharField(max_length=500, blank=True, null=True)
    post_created = models.DateTimeField(auto_now_add=True)
    post_edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reviewer', 'truck',)

    def __str__(self):
        return self.truck.title + ' - Review: ' + self.reviewer.username

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Invalid rating. Value must be between 0 and 5.")
        super()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Review, self).save(*args, **kwargs)

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
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visited = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = ('visited',)

    def __str__(self):
        return f'{self.truck.title} visited by {str(self.visitor.username)} | {self.visited.__str__()}'


class Live(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='live_objects')
    start_time = models.DateTimeField(auto_now_add=True, )
    end_time = models.DateTimeField()

    @property
    def live_time(self):
        f_mat = '%H:%M:%S'
        start = datetimefield_to_datetime(self.start_time)
        end = datetimefield_to_datetime(self.end_time)
        now = datetime.utcnow()
        if juxtapose(now) < juxtapose(end):
            sec = (now-start).total_seconds()

            return '{} hours'.format(time.strftime(f_mat, time.gmtime(sec)))
        else:
            sec = (end-start).total_seconds()
            return '{} hours'.format(time.strftime(f_mat, time.gmtime(sec)))

    def __str__(self):
        return f'{self.start_time} ----------> + {self.end_time}'
