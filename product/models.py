from django.core.exceptions import ValidationError
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


class Discount(models.Model):
    amount = models.CharField(max_length=20, )
    TYPES = (
        ('p', 'percent'),
        ('c', 'cash')
    )
    type1 = models.CharField(max_length=1, choices=TYPES)

    def __str__(self):
        return f'type: {self.type1}, amount: {self.amount}'


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
    discount = models.ForeignKey(Discount, blank=True, default=None, on_delete=models.DO_NOTHING)
    discount_price = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def is_price_after_discount(self):
        if self.discount and self.discount.type1 == 'p':
            new_price = self.price - (self.price * int(self.discount.amount)) / 100
            self.discount_price = new_price
            return True
        elif self.discount and self.discount.type1 == 'c':
            new_price = self.price - int(self.price)
            self.discount_price = new_price
            return True
        elif self.discount is None:
            return False

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug, ])
