from django.urls import path, include
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('apply/<int:order_id>/', views.CouponView.as_view(), name='apply_coupon'),
    path('pay/<int:order_id>/', views.Pay.as_view(), name='pay'),
    path('api/v1/', include('orders.api.v1.urls')),
]
