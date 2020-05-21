from django.db import models
from trucks.models import Truck
from users.models import User


# Possibly do something extremely similar for scheduling
class Event(models.Model):
    RECURRENCE_CHOICES = (
        (0, 'None'),
        (1, 'Daily'),
        (7, 'Weekly'),
        (14, 'Biweekly')
        # TODO need to change to base off DATETIME for > every last Friday of month, every Monday, exclude weekends ect.
    )

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    truck = models.ManyToManyField(Truck)
    frequency = models.IntegerField(choices=RECURRENCE_CHOICES)
    startTime = models.TimeField('Start Time')
    endTime = models.TimeField('End Time')
    startDate = models.DateField('Start Date')

    # TODO default endDate to ~ 2 years (or some timeframe) after startDate >
    #  so user doesn't destroy db with millions at once
    endDate = models.DateField('End Date')
    cancelledDate = models.DateField('Cancelled Date', blank=True, null=True)


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