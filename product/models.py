from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    code_no = models.CharField


class Category(models.Model):
    category_name = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Discount(models.Model):
    percent_discount = models.IntegerField
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class DiscountCode(models.Model):
    discount_code = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
