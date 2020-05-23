from django.test import TestCase

from trucks.models import Truck, MenuItem


class TruckTestCase(TestCase):
    def set_up(self):
        Truck.objects.create(title="New Truck One", description="To bring a wonderful fufilment of your taste buds!")
        Truck.objects.create(title="New Truck Two", description="To bring spice to you life and your block!")
        truck_one = Truck.objects.get(title="New Truck One")
        truck_two = Truck.objects.get(title="New Truck Two")
        self.assertEqual(truck_one.title[8], truck_two.title[8])


class MenuItemTestCase(TestCase):
    def set_up(self):
        Truck.objects.create(title="New Truck One")
        truck_one = Truck.objects.get(title="New Truck One")
        MenuItem.objects.create(name="Chicken Burrito", truck=truck_one, price=6.99,
                                description="Grilled chicken, wrapped in burrito with american cheese and tomatoes "
                                            "with black olives.")
        MenuItem.objects.create(name="Country Fried Chicken", truck=truck_one, price=9.99,
                                description="Deep-fried butter-milk chicken with smothered in white gravy.")
        menu = MenuItem.objects.filter(truck=truck_one)
        self.assertEqual(menu[0].name, "Chicken Burrito")
