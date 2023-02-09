from django.contrib import admin
from .models import Product, Category, Discount


admin.register(Product)(admin.ModelAdmin)
admin.register(Category)(admin.ModelAdmin)
admin.register(Discount)(admin.ModelAdmin)

