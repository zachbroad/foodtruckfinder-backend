import math
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import Q, Avg
from django.utils import timezone
from phone_field import PhoneField
from rest_framework.exceptions import ValidationError
from notifications.models import Notification

from util.models import ModelLocation

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
    title = models.CharField(null=False, blank=False,
                             unique=True, max_length=25)
    featured = models.BooleanField(default=False, blank=True)
    icon = models.ImageField(default=None, null=True,
                             blank=True, upload_to='uploads/tags/icons')

    class Meta:
        ordering = [
            'title'
        ]

    def __str__(self):
        return self.title


class Truck(ModelLocation):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', blank=True,
                              default='assets/truck_logo_placeholder.png')
    description = models.TextField(
        max_length=3000, blank=True, default='Sorry, this truck has no description')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact number')
    website = models.URLField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    available_for_catering = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @property
    def rating(self):
        rating = Review.objects.filter(truck=self).all(
        ).aggregate(Avg('rating'))['rating__avg']
        if rating is not None:
            return rating
        else:
            return None

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
        return len(self.live_objects.filter(start_time__lt=timezone.now(), end_time__gt=timezone.now())) > 0

    def __str__(self):
        return self.title


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
                              default='assets/truck_logo_placeholder.png')
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
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(verbose_name='truck_rating', validators=[
                                 validators.MinValueValidator(0), validators.MaxValueValidator(5)])
    description = models.TextField(max_length=2500, blank=True, null=True)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviewed_by')

    post_created = models.DateTimeField(auto_now_add=True)
    post_edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reviewer', 'truck',)

    def __str__(self):
        return self.truck.title + ' - Review: ' + self.reviewer.username

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError(
                "Invalid rating. Value must be between 0 and 5.")
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


class ReviewLike(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(null=False, blank=False)
    liked_by = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_by')

    def __str__(self):
        if self.is_liked:
            liked = ' - Liked by: '
        else:
            liked = ' - Disliked by: '
        return str(self.review) + liked + str(self.liked_by)


class Visit(models.Model):
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='visits')
    visitor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visited_by')
    visited = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = ('visited',)

    def __str__(self):
        return f'{self.truck.title} visited by {str(self.visitor.username)} | {self.visited.__str__()}'


class Live(models.Model):
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name='live_objects')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    @property
    def live_time(self):
        f_mat = '%H:%M:%S'
        start = self.start_time
        end = self.end_time
        now = timezone.now()
        if now < end:
            sec = (now - start).total_seconds()
            return '{}'.format(time.strftime(f_mat, time.gmtime(sec)))
        else:
            sec = (end - start).total_seconds()
            return '{}'.format(time.strftime(f_mat, time.gmtime(sec)))

    @property
    def live(self):
        try:
            why = self.start_time < timezone.now() < self.end_time
            return why
        except Exception as e:
            if e == Live.DoesNotExist:
                return False
        return False

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError('Start time must be before end time')
        if timezone.now() < self.end_time:
            lives = Live.objects.filter(
                (Q(start_time__lte=self.end_time, end_time__gte=self.start_time)) & Q(truck__id=self.truck.pk))
            editing = lives[0].pk == self.pk
            if lives.exists() and not editing:
                raise ValidationError(
                    'You are already live, or will be live during this time')
        else:
            raise ValidationError(
                'Can not have end time before the start time')

        super(Live, self).clean()

    def __str__(self):
        return f'{self.start_time} ----------> + {self.end_time}'


@receiver(post_save, sender=Live)
def notify_on_live_creation(sender, instance, created, **kwargs):
    if created:
        notif = Notification.objects.create(title='{} went live!'.format(instance.truck.title), description='{} went live, and plans to be live until {}'.format(
            instance.truck.title, instance.end_time), user=instance.truck.owner, route='/trucks/profile/{}'.format(instance.truck.pk))
        notif.save()
