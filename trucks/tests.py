from django.test import TestCase

from trucks.models import Truck, MenuItem


class TruckTestCase(TestCase):
    def setUp(self) -> None:
        self.truck = Truck.objects.create(title="New Truck One", description="To bring a wonderful fulfilment of your taste buds!")

    def test_has_image(self):
        self.assertIs(self.truck.image.name, Truck._meta.get_field('image').get_default())
        self.truck.image = None
        self.assertIsNone(self.truck.image.name)


class MenuItemTestCase(TestCase):
    def setUp(self) -> None:
        Truck.objects.create(title="New Truck One")
        self.truck_one = Truck.objects.get(title="New Truck One")
        MenuItem.objects.create(name="Chicken Burrito",
                                truck=self.truck_one,
                                price=6.99,
                                description="Grilled chicken, wrapped in burrito with american cheese and tomatoes with black olives.")
        MenuItem.objects.create(name="Country Fried Chicken",
                                truck=self.truck_one,
                                price=9.99,
                                description="Deep-fried butter-milk chicken with smothered in white gravy.")

    def test_menu_item_name(self):
        menu = MenuItem.objects.filter(truck=self.truck_one)
        self.assertEqual(menu[0].name, "Chicken Burrito")
        self.assertEqual(menu[1].name, "Country Fried Chicken")
