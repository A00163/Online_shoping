from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.first_name


class Address(models.Model):
    city_name = models.CharField(max_length=30)
    street_name = models.CharField(max_length=30)
    # plock_no = models.IntegerField(max_length=3)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
