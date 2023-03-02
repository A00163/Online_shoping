from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token_view

urlpatterns = [
    path('api-token-auth/', auth_token_view.obtain_auth_token),
    path('create/', views.OrderCreateAPIView.as_view()),
    path('cart/add/', views.AddToCartAPIView.as_view()),
    path('detail/<int:order_id>/', views.OrderDetailAPIView.as_view()),
    # path('detail/<int:order_id>/', views.OrderDetailAPIView.as_view())
]
