from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from .cart import Cart
from .forms import CartAddForm, CouponForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItems, Coupon
import datetime
from django.contrib import messages

class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order.html'
    form = CouponForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order': order, 'form': self.form})


class OrderCreateView(LoginRequiredMixin, View):
    template_name = 'orders:order_detail'

    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItems.objects.create(order=order, product=item['product'], price=item['price'],
                                      quantity=item['quantity'])
        cart.clear()
        return redirect(self.template_name, order.id)


class CouponView(LoginRequiredMixin, View):
    form = CouponForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exist', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)


