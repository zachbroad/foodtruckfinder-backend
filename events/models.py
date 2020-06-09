from django.db import models
from trucks.models import Truck
from users.models import User
from django_google_maps import fields as map_fields
import googlemaps
from django.conf import settings


# Possibly TODO do something extremely similar for scheduling
class Event(models.Model):
    RECURRENCE_CHOICES = (
        (0, 'None'),
        (1, 'Daily'),
        (7, 'Weekly'),
        (14, 'Biweekly')
        # TODO need to change to base off DATETIME for > every last Friday of month, every Monday, exclude weekends ect.
    )

    title = models.CharField(max_length=120)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_organizer')
    description = models.CharField(
        max_length=500, blank=True, default='Sorry, this truck has no description')
    address = map_fields.AddressField(max_length=200, blank=True, null=True, verbose_name='address')
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True, verbose_name='geolocation')
    truck = models.ManyToManyField(Truck, related_name='events')
    frequency = models.IntegerField(choices=RECURRENCE_CHOICES)
    start_time = models.TimeField('Start Time')
    end_time = models.TimeField('End Time')
    start_date = models.DateField('Start Date')

    # TODO default endDate to ~ 2 years (or some time-frame) after startDate ->
    #  so user doesn't destroy db with millions at once
    end_date = models.DateField('End Date')
    cancelledDate = models.DateField('Cancelled Date', blank=True, null=True)

    def save(self, *args, **kwargs):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        # Check if address not given when geolocation is
        if self.address is None and self.geolocation is not None:
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

        try:
            if self.geolocation is None:
                resp = gmaps.geocode(self.address)
                location = resp[0]['geometry']['location']
                self.geolocation = "{},{}".format(location['lat'], location['lng'])
        except Exception:
            pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CancelledEventManager(models.Manager):
    def get_query_set(self):
        return self.filter(cancelledDate__isnull=False)


class CancelledEvent(Event):
    class Meta:
        proxy = True

    objects = CancelledEventManager()


# class PaidLessonManager(models.Manager):
#     def get_query_set(self):
#         return self.filter(paidDate__isnull=False)
#
#
# class PaidEvent(Event):
#     class Meta:
#           proxy = True
#
#     objects = PaidLessonManager()
