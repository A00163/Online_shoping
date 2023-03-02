from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.models import Address
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

    def post(self, request):
        cart = Cart(request)
        product = get_object_or_404(Product, id=request.POST.get('item_id'))
        quantity = int(request.POST.get('quantity'))
        cart.update(product, quantity)
        return redirect('orders:cart')


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('product:home')


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
        addresses = Address.objects.filter(customer_id=request.user.id)

        # context = {
        #     "addresses": Address.objects.filter(customer_id=request.user.id)
        # }
        return render(request, self.template_name, {'order': order, 'form': self.form, 'addresses': addresses})


class OrderCreateView(LoginRequiredMixin, View):
    template_name = 'orders:order_detail'

    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        order.save()
        for item in cart:
            order_item = OrderItems.objects.create(product=item['product'], order=order, price=item['price'],
                                                   quantity=item['quantity'])
            order_item.save()

        cart.clear()
        return redirect(self.template_name, order.id)


# class ClearCartViews(View):
#     def get(self, request):


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
