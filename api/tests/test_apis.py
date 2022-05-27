import json
import uuid
from rest_framework import status
from django.test import TestCase, Client
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
    def setUp(self):
        self.item1 = Product.objects.create(
            name="Test Item1", price=250, quantity=4, category="Stationary")
        self.item2 = Product.objects.create(
            name="Test Item2", price=200, quantity=4, category="Toys")

    def test_get_single_product(self):
        response = client.get(
            reverse('single-product', kwargs={'pk': self.item2.pk}))
        product = Product.objects.get(pk=self.item2.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_product(self):
        random_uuid = str(uuid.uuid4())
        response = client.get(
            reverse('single-product', kwargs={'pk': random_uuid}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class createNewProductTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            'name': 'Test Item',
            'description': 'create new product to test',
            'quantity': 12,
            'price': 100,
            'category': 'Grocery'
        }
        self.invalid_payload = {
            'name': '',
            'quantity': 10,
            'category': 'Electronics',
            'price': 500
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('products'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('products'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class updateSingleProductTest(TestCase):

    def setUp(self):
        self.test_item = Product.objects.create(
            name="Test Item", quantity=3, price=70, category="Grocery")
        self.valid_payload = {
            "name": "Test Item",
            "quantity": 4,
            "price": 80,
            "category": "Grocery"
        }
        self.invalid_payload = {
            "name": "",
            "quantity": 4,
            "price": 70,
            "category": "Grocery"
        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('single-product', kwargs={'pk': self.test_item.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_product_update(self):
        response = client.put(
            reverse('single-product', kwargs={'pk': self.test_item.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleProduct(TestCase):

    def setUp(self):
        self.item = Product.objects.create(
            name="Test Delete Item", price=10, quantity=20, category="Electronics")

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('single-product', kwargs={'pk': self.item.pk})).json()
        self.assertEqual(response['message'], f"Product with id {self.item.pk} has been deleted")

    def test_invalid_delete_product(self):
        random_uuid = str(uuid.uuid4())
        response = client.delete(
            reverse('single-product', kwargs={'pk': random_uuid})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
