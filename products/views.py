from django.shortcuts import render
from .models import Product

# Create your views here.

def products_dashboard(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'dashboard.html', context)
