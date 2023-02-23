from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, OrderItemSerializer, ProductSerializer
from rest_framework.exceptions import ValidationError, ParseError

from orders.cart import Cart
from orders.models import Order, OrderItems
from product.models import Product


class AddToCartAPIView(APIView):
    def post(self, request):
        cart = Cart(request)
        ser_data = ProductSerializer(data=request.data)
        if ser_data.is_valid():
            product = get_object_or_404(Product, id=ser_data.validated_data['product_id'])
            quantity = ser_data.validated_data['quantity']
            cart.add(product, int(quantity))
            print(cart.cart.items())
            data = {'message': f'your order item added  successfully.'}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=ser_data.errors)


class OrderCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        cart = Cart(request)
        print(cart.cart.items())
        order = Order.objects.create(user=request.user)
        order.save()
        for item in cart:
            print(item)
            # product = get_object_or_404(Product, id=int(item['id']))
            id_product = int(item['id_product'])
            print(id_product)
            product = Product.objects.get(pk=id_product)
            quantity = int(item['quantity'])
            price = int(item['price'])
            order_item = OrderItems.objects.create(order=order, product=product, quantity=quantity, price=price)
            order_item.save()

        cart.clear()
        data = {'message': f'your order was registered successfully.\n order cod:{order.id}'}
        return Response(data=data, status=status.HTTP_201_CREATED)

# class OrderDetailAPIView:
#     pass

