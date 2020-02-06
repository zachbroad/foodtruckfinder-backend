from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
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
    image = models.ImageField(upload_to='uploads/trucks/profile-pictures', blank=True,
                              default='../media/uploads/trucks/profile-pictures/truck_logo_placeholder.png')
    description = models.CharField(
        max_length=500, blank=True, default='Sorry, this truck has no description')
    location = PlainLocationField(based_fields=['city'], zoom=7, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
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

    # specific

    # TODO: #

    # query choices by current truck field in admin panel #
    entre = models.ForeignKey('self', on_delete=models.CASCADE, limit_choices_to={
                              'type': 1, }, null=True, blank=True, related_name='item1')
    side = models.ForeignKey('self', on_delete=models.CASCADE, limit_choices_to={
                             'type': 2, }, null=True, blank=True, related_name='item2')
    drink = models.ForeignKey('self', on_delete=models.CASCADE, limit_choices_to={
                              'type': 3, }, null=True, blank=True, related_name='item3')
    desert = models.ForeignKey('self', on_delete=models.CASCADE, limit_choices_to={
                               'type': 4, }, null=True, blank=True, related_name='item4')

    def clean_item(self):
        if self.entre != None:
            raise ValidationError(
                'You must set the type to combo to add to the Entre items field.')
        if self.side != None:
            raise ValidationError(
                'You must set the type to combo to add to the Side items field.')
        if self.drink != None:
            raise ValidationError(
                'You must set the type to combo to add to the Drink items field.')
        if self.desert != None:
            raise ValidationError(
                'You must set the type to combo to add to the Desert items field.')

    # TODO: #
    # Validate all types #
    def clean(self) -> None:
        if self.type == MenuItem.TYPE_ENTRE:
            if self.entre != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Entre items field.')
            if self.side != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Side items field.')
            if self.drink != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Drink items field.')
            if self.desert != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Desert items field.')

        elif self.type == MenuItem.TYPE_SIDE:
            if self.entre != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Entre items field.')
            if self.side != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Side items field.')
            if self.drink != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Drink items field.')
            if self.desert != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Desert items field.')

        elif self.type == MenuItem.TYPE_DRINK:
            if self.entre != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Entre items field.')
            if self.side != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Side items field.')
            if self.drink != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Drink items field.')
            if self.desert != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Desert items field.')

        elif self.type == MenuItem.TYPE_DESERT:
            if self.entre != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Entre items field.')
            if self.side != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Side items field.')
            if self.drink != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Drink items field.')
            if self.desert != None:
                raise ValidationError(
                    'You must set the type to combo to add to the Desert items field.')

        elif self.type == MenuItem.TYPE_COMBO:
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
