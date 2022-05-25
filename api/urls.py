from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/<str:pk>', views.single_product, name='single-product'),
]
