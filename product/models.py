from django.db import models

from django.contrib.auth.models import User

from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:category_filter', args=[self.slug, ])


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug, ])


class Discount(models.Model):
    percent_discount = models.IntegerField()
    value_discount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.percent_discount)


class DiscountCode(models.Model):
    discount_code = models.CharField(max_length=15)
    order = models.ForeignKey(Product, on_delete=models.CASCADE)
