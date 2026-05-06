from django.contrib import admin
from .models import ProductCategory, Buyer, Product, Order, Review

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'bonuses')
    search_fields = ('full_name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'size', 'price', 'availability')
    list_filter = ('category',)
    search_fields = ('description',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'date_of_creation', 'payment', 'delivery_option', 'registration_status')
    list_filter = ('payment', 'delivery_option', 'registration_status')
    filter_horizontal = ('products',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'rating', 'date_of_publication', 'status')
    list_filter = ('rating', 'status')