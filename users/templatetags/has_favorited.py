from django import template

from trucks.models import TruckFavorite, Truck

register = template.Library()


@register.filter()
def has_favorited_truck(value, arg):
    try:
        truck = Truck.objects.get(id=arg)
        return TruckFavorite.objects.get(truck=truck, user=value) != None
    except Exception as e:
        print(e)
        return False
