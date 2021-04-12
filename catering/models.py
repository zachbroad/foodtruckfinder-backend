from django.db import models
from phone_field import PhoneField

# Create your models here.
from trucks.models import Truck


class CaterRequest(models.Model):
    name = models.CharField(max_length=128, help_text='Your name and/or event name')
    email = models.EmailField(help_text='Email you\'d like to be reached at')
    phone = PhoneField(help_text='Your contact number')
    details = models.TextField(max_length=10000, help_text='Tell us about your event')
    truck = models.ForeignKey(Truck, on_delete=models.DO_NOTHING,
                              help_text='What truck would you like to cater your event?', related_name='cater_requests')

    when = models.DateTimeField(help_text='When is your event?')
    duration = models.FloatField(help_text='How many hours do you want catering?')

    requested_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-when',)

    def __str__(self):
        return 'Cater request by {} for truck {} at {} for {} hours'.format(self.name, self.truck, self.when,
                                                                            self.duration)
