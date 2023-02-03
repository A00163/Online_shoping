from django.test import TestCase
from product.models import Product, Category, Discount


class CategoryTestCase(TestCase):
    def test_fields_product_name(self):
        phones = Category.objects.create(name='phone')
        phones.save()
        self.assertEqual(str(phones), 'phone')


class ProductTestCase(TestCase):

    def test_products(self):
        accessories = Category.objects.create(name="accessories")
        accessories.save()
        headphone = Product.objects.create(title="Galaxy buds live", price=1800, category=accessories)
        headphone.save()
        headphone2 = Product.objects.create(title="air-pod", price=2800, category=accessories)
        headphone2.save()
        record = Product.objects.get(id=1)
        self.assertEqual(record.category.name, "accessories")


class DiscountTestCase(TestCase):
    def test_discount(self):
        category = Category.objects.create(name='laptop')
        category.save()
        product = Product.objects.create(title='lenovo id_pad', price=3000, category=category)
        product.save()
        discount = Discount(percent_discount=int(5), product=product)
        discount.save()
        self.assertEqual(discount.product.title, 'lenovo id_pad')
