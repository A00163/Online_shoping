from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product


class HomeView(View):
    template_name = 'product/index.html'

    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, self.template_name, {'products': products})

    def post(self, request):
        return render(request, self.template_name)


class ProductDetailView(View):
    template_name = 'product/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, self.template_name, {'product': product})
