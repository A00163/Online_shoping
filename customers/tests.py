from django.test import TestCase

from customers.models import Customer, Address


class CustomerTestCase(TestCase):

    def test_customer(self):
        customer = Customer(first_name='maryam', last_name='amini', email="abc@gmail.com")
        customer.save()
        self.assertEqual(str(customer), "maryam")

    def test_address(self):
        customer = Customer(first_name='sepehr', last_name='amini', email="abc@gmail.com")
        customer.save()
        address = Address(city_name='Tehran', street_name='Keshavarz', customer=customer)
        address.save()
        self.assertEqual(str(address.customer), "sepehr")
