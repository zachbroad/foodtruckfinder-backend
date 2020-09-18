from django.db import models
from phone_field import PhoneField

from grubtrucks.settings.settings import AUTH_USER_MODEL
from trucks.models import Truck
from users.models import User
from util.models import ModelLocation


class Event(ModelLocation):
    title = models.CharField(max_length=120, help_text='Event name')
    description = models.TextField(max_length=3000, blank=True, default='Sorry, this event has no description',
                                   help_text='Event description')
    trucks = models.ManyToManyField(Truck, related_name='events', blank=True, null=True, help_text='What trucks are attending?')
    start_time = models.DateTimeField(help_text='When does the event begin?')
    end_time = models.DateTimeField(help_text='When does the event end?')
    phone_number = PhoneField(null=True, blank=True, help_text="Event organizer's contact number")
    organizer = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, help_text='Event organizer', on_delete=models.CASCADE)

    cancelled_date = models.DateField('Cancelled Date', blank=True, null=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ImGoing(models.Model):
    comments = models.TextField(max_length=500, help_text='Is there anything you\'d like to say to the event organizer?', blank=True,
                                null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text='Event you are attending')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='Who is going?')

    class Meta:
        unique_together = ('event', 'user',)


class CancelledEventManager(models.Manager):
    def get_query_set(self):
        return self.filter(cancelled_date__isnull=False)


class CancelledEvent(Event):
    class Meta:
        proxy = True

    objects = CancelledEventManager()
