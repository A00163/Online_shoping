from django.urls import path

from product import views
app_name = 'product'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail')
]
