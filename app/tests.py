from django.test import TestCase
from django.test import TestCase
from .models import ProductCategory, Buyer

class ModelTests(TestCase):
    def test_category_creation(self):
        cat = ProductCategory.objects.create(title="Обувь", description="Разная обувь")
        self.assertEqual(str(cat), "Обувь")
    
    def test_buyer_creation(self):
        buyer = Buyer.objects.create(
            full_name="Иван Петров",
            email="ivan@example.com",
            phone="+71234567890",
            address="Москва"
        )
        self.assertEqual(buyer.bonuses, 0)
# Creae your tests here.
