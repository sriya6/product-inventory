from django.test import TestCase
from .models import Product

# Create your tests here.

class ProductTest(TestCase):
    def setUp(self):
        Product.objects.create(
            name='Apple', description='fruit', price=50, quantity=50, category='Grocery'
        )
        Product.objects.create(
            name='Test item', price=500, quantity=3, category='Electronics'
        )

    def test_product(self):
        apple = Product.objects.get(name='Apple')
        test_item = Product.objects.get(name='Test item')
        self.assertEqual(apple.get_count(), "50 items in stock")
        self.assertEqual(test_item.get_count(), "3 items in stock")
