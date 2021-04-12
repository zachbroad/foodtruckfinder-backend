import googlemaps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_google_maps import fields as map_fields


class ModelLocation(models.Model):
    class Meta:
        abstract = True

    address = map_fields.AddressField(max_length=200, blank=True, null=True, verbose_name='address')
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True, verbose_name='geolocation')

    # def save(self, *args, **kwargs):
    #     g_maps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    #
    #     # Check if address not given when geolocation is
    #     if self.address is None and self.geolocation is not None:
    #         points = self.geolocation.split(',')
    #         lat, lng = points[0], points[1]
    #         resp = g_maps.reverse_geocode((float(lat), float(lng)))
    #
    #         address_components = resp[0]['address_components']
    #         city_name = address_components[2]['long_name']
    #         country_abbr = address_components[5]['short_name']
    #         house_number = address_components[0]['long_name']
    #         state_abbr = address_components[4]['short_name']
    #         street_name = address_components[1]['long_name']
    #
    #         self.address = "{} {}, {}, {}, {}".format(house_number, street_name, city_name, state_abbr, country_abbr)
    #
    #     try:
    #         if self.geolocation is None:
    #             resp = g_maps.geocode(self.address)
    #             location = resp[0]['geometry']['location']
    #             self.geolocation = "{},{}".format(location['lat'], location['lng'])
    #     except Exception:
    #         pass
    #
    #     super().save(*args, **kwargs)


class GenericImage(models.Model):
    image = models.ImageField(upload_to='images')
    caption = models.CharField(max_length=1024, blank=True, null=True)

    content_object = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    def __str__(self):
        return self.image.name
