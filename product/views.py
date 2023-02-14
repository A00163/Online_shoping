from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Category
from orders.forms import CartAddForm


class HomeView(View):
    template_name = 'product/index.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, self.template_name, {'products': products, 'categories': categories})

    def post(self, request):
        return render(request, self.template_name)


class ProductDetailView(View):
    template_name = 'product/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, self.template_name, {'product': product, 'form': form})
