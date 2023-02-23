from django.urls import path
from django.contrib import admin
# from django.conf import settings
from accounts import views
app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCode.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('edit_user/', views.EditUserView.as_view(), name='edit_user'),
    path('addresses/', views.AddressUserView.as_view(), name='addresses_user'),
    path('password/', views.ChangePasswordView.as_view(template_name='accounts/change_password.html'),
         name='change_password'),
    path('addresses/edit_address/<int:address_id>/', views.EditAddressView.as_view(), name='edit_address'),
    path('addresses/remove_address/<int:address_id>/', views.RemoveAddressView.as_view(), name='remove_address'),
    path('addresses/add_address/', views.AddAddressView.as_view(), name='add_address'),
    path('orders_history/', views.OrdersHistoryView.as_view(), name='orders_history'),
    path('detail_order/<int:order_id>/', views.OrdersDetailView.as_view(), name='detail_order')

]
