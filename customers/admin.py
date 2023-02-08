from django.contrib import admin
from .models import Customer, Address

admin.register(Customer)(admin.ModelAdmin)
admin.register(Address)(admin.ModelAdmin)
