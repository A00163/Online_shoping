from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=30)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product/static/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Discount(models.Model):
    percent_discount = models.IntegerField()
    value_discount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.percent_discount)


class DiscountCode(models.Model):
    discount_code = models.CharField(max_length=15)
    order = models.ForeignKey(Product, on_delete=models.CASCADE)
