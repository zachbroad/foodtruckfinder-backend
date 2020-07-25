from django.db import models

from util.models import ModelLocation
from trucks.models import Truck
from users.models import User


class Event(ModelLocation):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=3000, blank=True, default='Sorry, this event has no description')
    trucks = models.ManyToManyField(Truck, related_name='events', blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    cancelled_date = models.DateField('Cancelled Date', blank=True, null=True)

    # GenericImage.objects.filter(content_object=self).all()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CancelledEventManager(models.Manager):
    def get_query_set(self):
        return self.filter(cancelled_date__isnull=False)


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
