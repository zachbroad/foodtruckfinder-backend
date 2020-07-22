from django.db import models
from trucks.models import Truck, ModelLocation
from users.models import User
from django_google_maps import fields as map_fields
import googlemaps
from django.conf import settings


class Event(ModelLocation):

    title = models.CharField(max_length=120)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_organizer', null=True)
    description = models.CharField(max_length=500, blank=True, default='Sorry, this event has no description')
    trucks = models.ManyToManyField(Truck, related_name='events')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    cancelled_date = models.DateField('Cancelled Date', blank=True, null=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

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
