import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from products.models import Product
from ..serializers import ProductSerializer

client = Client()

class getAllProductsTest(TestCase):

    def setUp(self):
        Product.objects.create(
            name="Test1", price=100, quantity=10, category="Grocery")
        Product.objects.create(
            name="Test2", price=200, quantity=20, category="Electronics")
        Product.objects.create(
            name="Test3", price=400, quantity=4, category="Books")
        Product.objects.create(
            name="Test4", price=500, quantity=5, category="Stationary")

    def test_get_all_products(self):
        response = client.get(reverse("products"))

        # get data from database
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class getSingleProductTest(TestCase):
    # TODO
    pass

class createNewProductTest(TestCase):
    # TODO
    pass

class updateSingleProduct(TestCase):
    # TODO
    pass

class DeleteSingleProduct(TestCase):
    # TODO
    pass
