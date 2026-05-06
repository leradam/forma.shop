from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Buyer(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    bonuses = models.IntegerField(default=0)
    # Связь с пользователем Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    size = models.IntegerField()
    description = models.TextField()
    availability = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.category.title} - {self.size}"

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    date_of_creation = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=200, verbose_name="Способ оплаты")
    delivery_option = models.CharField(max_length=200, verbose_name="Способ доставки")
    registration_status = models.CharField(max_length=200, verbose_name="Статус заказа")
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.buyer.full_name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    review_text = models.TextField()
    date_of_publication = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, verbose_name="Статус отзыва")

    def __str__(self):
        return f"Отзыв от {self.buyer.full_name} на {self.product}"