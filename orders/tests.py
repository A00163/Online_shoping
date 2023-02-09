from django.test import TestCase

from accounts.models import User
from orders.models import OrderItems, Order
from product.models import Product, Category


class OrderTestCase(TestCase):
    def test_order(self):
        customer = User.objects.create(first_name='atefe', last_name='mohammadi',
                                       email='aalimohammadi00163@gmail.com')
        customer.save()
        order = Order(customer=customer)
        order.save()
        self.assertEqual(str(order), 'atefe')


class OrderItemTestCase(TestCase):
    def test_order_item(self):
        category = Category.objects.create(name='electrical')
        category.save()
        product1 = Product.objects.create(title='flash', price=600, category=category)
        product1.save()
        customer = User.objects.create(first_name='sara', last_name='mohammadi',
                                       email='aalimohammadi00163@gmail.com')
        customer.save()
        order = Order(customer=customer)
        order.save()
        order_item1 = OrderItems.objects.create(product=product1, order=order)
        order_item1.save()
        self.assertEqual(order_item1.product.title, 'flash')
        self.assertEqual(order_item1.order.customer.first_name, 'sara')
