from django.urls import path

from product import views

urlpatterns = [
    path('index', views.index)
]
