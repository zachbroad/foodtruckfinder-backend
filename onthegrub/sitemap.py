from django.urls import path

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from trucks.models import Review, Truck

truck_info_dict = {
    'queryset': Truck.objects.all(),
    'date_field': 'last_updated'
}

review_info_dict = {
    'queryset': Review.objects.all(),
    'date_field': 'post_edited',
}
sitemap = path("sitemap.xml", sitemap, {
    'sitemaps': {
        'trucks': GenericSitemap(info_dict=truck_info_dict, priority=1.0),
        'reviews': GenericSitemap(info_dict=review_info_dict, priority=0.9)
    }
}, name="django.contrib.sitemaps.views.sitemap", ),
