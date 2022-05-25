import uuid
from django.db import models

class Product(models.Model):
    CATEGORY = (
        ('Grocery', 'Grocery'),
        ('Stationary', 'Stationary'),
        ('Electronics', 'Electronics'),
        ('Books', 'Books'),
        ('Toys', 'Toys')
    )
    name = models.CharField(max_length=200, help_text="Enter Product Name")
    description = models.TextField(help_text="Enter Product Description", null=True, blank=True)
    featured_image = models.ImageField(default='default.jpg', null=True, blank=True)
    price = models.FloatField(help_text="Enter Product Price per unit")
    quantity = models.IntegerField(help_text="Enter Product Quantity in stock")
    category = models.CharField(max_length=50, choices=CATEGORY, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
        editable=False)

    def get_count(self):
        return self.quantity + " items in stock"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
