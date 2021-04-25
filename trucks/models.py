import math
import time

from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import Q, Avg, Count, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from phone_field import PhoneField
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

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

TYPE_NONE = 0
TYPE_ENTRE = 1
TYPE_SIDE = 2
TYPE_DRINK = 3
TYPE_DESSERT = 4
TYPE_COMBO = 5

TYPE_CHOICES = [
    (TYPE_NONE, 'None'),
    (TYPE_ENTRE, 'Entre'),
    (TYPE_SIDE, 'Side'),
    (TYPE_DRINK, 'Drink'),
    (TYPE_DESSERT, 'Desert'),
    (TYPE_COMBO, 'Combo')
]


class Tag(models.Model):
    title = models.CharField(null=False, blank=False, unique=True, max_length=25)
    featured = models.BooleanField(default=False, blank=True)
    icon = models.ImageField(default=None, null=True, blank=True, upload_to='uploads/tags/icons')

    class Meta:
        ordering = [
            'title'
        ]

    def __str__(self):
        return self.title


class TruckFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_trucks')
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name='favorites')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'truck')

    def __str__(self):
        return '{} favorited by {}'.format(self.truck.title, self.user.username)


class TruckEvent(ModelLocation):
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name='schedule', related_query_name='schedule')

    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return "{}'s event ({}) @ {} until {}".format(self.truck.title, self.title or "unnamed", self.start_time,
                                                      self.end_time)

    def get_absolute_url(self):
        return reverse('trucks:event-detail', args=[self.truck_id, self.id])

    @property
    def has_ended(self) -> bool:
        return (self.end_time - timezone.now()).total_seconds() < 0

    @property
    def is_now(self) -> bool:
        return self.start_time < timezone.now() < self.end_time


class TruckQuerySet(models.QuerySet):
    def live(self):
        return self.filter(live_objects__start_time__lt=timezone.now(),
                           live_objects__end_time__gt=timezone.now()).all()

    def caterers(self):
        return self.filter(available_for_catering=True)

    def user_trucks(self, user):
        return self.filter(owner=user)


class TruckManager(models.Manager):
    def get_queryset(self):
        return TruckQuerySet(self.model, using=self._db)

    def get_live(self):
        return self.get_queryset().live()

    def get_caterers(self):
        return self.get_queryset().caterers()

    def get_user_trucks(self, user):
        return self.get_queryset().user_trucks(user)


class Truck(ModelLocation):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', blank=True, null=False,
                              default='../media/assets/truck_logo_placeholder.png')
    description = models.TextField(max_length=3000, blank=True, default='Sorry, this truck has no description.')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    phone = PhoneField(blank=True, help_text='Contact number')
    website = models.URLField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    available_for_catering = models.BooleanField(default=False)

    last_updated = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(default=False)
    objects = TruckManager()

    def get_absolute_url(self):
        return reverse("trucks:detail", args=[self.id])

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @property
    def rating(self):
        rating = Review.objects.filter(truck=self).all().aggregate(Avg('rating'))['rating__avg']
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
        try:
            return Truck.distance_raw(float(lat), float(lng), float(self.geolocation.lat), float(self.geolocation.lon))
        except:
            return None

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
    def visit_count(self):
        return self.visits.count

    @property
    def reviews(self):
        return self.review.all()

    @property
    def is_favorited(self):
        return TruckFavorite.objects.get(truck_id=self.id).exists()

    @property
    def live(self):
        return self.live_objects.filter(start_time__lt=timezone.now(),
                                        end_time__gt=timezone.now()).exists() or self.schedule.filter(
            start_time__lt=timezone.now(), end_time__gt=timezone.now()).exists()

    @staticmethod
    def get_trending():
        trucks = Truck.objects.all()
        trending = trucks.annotate(favorite_count=Count(F('favorites'))).order_by('-favorite_count')
        return trending

    @property
    def upcoming_schedule(self) -> [TruckEvent]:
        return self.schedule.filter(start_time__gte=timezone.now())

    def __str__(self):
        return self.title


class TruckImage(models.Model):
    truck = models.ForeignKey(Truck, help_text='Truck this image belongs to', related_name='images',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='truck_images')
    caption = models.CharField(max_length=1024, blank=True, null=True, help_text='Image caption')

    def __str__(self):
        return self.image.name


class MenuItemQuerySet(models.QuerySet):
    def uncategorized(self):
        self.filter(type=TYPE_NONE).all()

    def entres(self):
        self.filter(type=TYPE_ENTRE).all()

    def drinks(self):
        self.filter(type=TYPE_DRINK).all()

    def sides(self):
        self.filter(type=TYPE_SIDE).all()

    def desserts(self):
        self.filter(type=TYPE_DESSERT).all()

    def combos(self):
        self.filter(type=TYPE_COMBO).all()


class MenuItemManager(models.Manager):
    def get_queryset(self):
        return MenuItemQuerySet(self.model, using=self._db)

    def get_uncategorized(self):
        return self.get_queryset().uncategorized()

    def get_entres(self):
        return self.get_queryset().entres()

    def get_sides(self):
        return self.get_queryset().sides()

    def get_drinks(self):
        return self.get_queryset().drinks()

    def get_desserts(self):
        return self.get_queryset().desserts()

    def get_combos(self):
        return self.get_queryset().combos()


class MenuItem(models.Model):
    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_NONE)

    # non-specific
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=120, blank=False)
    description = models.CharField(max_length=500, blank=True, )
    price = models.FloatField(max_length=10)
    image = models.ImageField(upload_to='uploads/trucks/menu-items', null=False, blank=True,
                              default='/assets/truck_logo_placeholder.png')
    featured = models.BooleanField(default=False)

    objects = MenuItemManager()

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
    rating = models.IntegerField(verbose_name='truck_rating',
                                 validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)])
    description = models.TextField(max_length=2500, blank=True, null=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviewed_by')

    post_created = models.DateTimeField(auto_now_add=True)
    post_edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reviewer', 'truck',)

    def __str__(self):
        return self.truck.title + ' - Review: ' + self.reviewer.username

    def get_absolute_url(self):
        return reverse("trucks:review-detail", args=[self.truck_id, self.id])

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Review, self).save(*args, **kwargs)

    @property
    def likes(self):
        return self.likes.all().filter(is_liked=True)

    @property
    def dislikes(self):
        return self.likes.all().filter(is_liked=False)


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(null=False, blank=False)
    liked_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_by')

    def __str__(self):
        if self.is_liked:
            liked = ' - Liked by: '
        else:
            liked = ' - Disliked by: '
        return str(self.review) + liked + str(self.liked_by)


class Visit(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='visits')
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visited_by')
    visited = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = ('visited',)

    def __str__(self):
        return f'{self.truck.title} visited by {str(self.visitor.username)} | {self.visited.__str__()}'

    @staticmethod
    def owner_visits(user):
        return Visit.objects.filter(truck__owner=user).count


class Live(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='live_objects')
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
                raise ValidationError('You are already live, or will be live during this time')
        else:
            raise ValidationError('Can not have end time before the start time')

        super(Live, self).clean()

    def __str__(self):
        return f'{self.start_time} ----------> + {self.end_time}'


@receiver(post_save, sender=Live)
def notify_on_live_creation(sender, instance, created, **kwargs):
    if created:
        notif = Notification.objects.create(title='{} went live!'.format(instance.truck.title),
                                            description='{} went live, and plans to be live until {}'.format(
                                                instance.truck.title, instance.end_time), user=instance.truck.owner,
                                            route='/trucks/profile/{}'.format(instance.truck.pk))
        notif.save()
