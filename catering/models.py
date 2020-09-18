from django.db import models

# Create your models here.
from trucks.models import Truck


class CaterRequest(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    details = models.TextField(max_length=10000)
    truck = models.ForeignKey(Truck, on_delete=models.DO_NOTHING)

    when = models.DateTimeField()
    duration = models.FloatField()

    requested_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-when',)

    def __str__(self):
        return 'Cater request by {} for truck {} at {} for {} hours'.format(self.name, self.truck, self.when, self.duration)
