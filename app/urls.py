from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # Главная страница
    path('', views.HomeView.as_view(), name='home'),

    # Регистрация и авторизация
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Корзина и заказы
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/<int:quantity>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Категории товаров
    path('categories/', views.ProductCategoryListView.as_view(), name='productcategory_list'),
    path('categories/<int:pk>/', views.ProductCategoryDetailView.as_view(), name='productcategory_detail'),
    path('categories/create/', views.ProductCategoryCreateView.as_view(), name='productcategory_create'),
    path('categories/<int:pk>/edit/', views.ProductCategoryUpdateView.as_view(), name='productcategory_update'),

    # Покупатели
    path('buyers/', views.BuyerListView.as_view(), name='buyer_list'),
    path('buyers/<int:pk>/', views.BuyerDetailView.as_view(), name='buyer_detail'),
    path('buyers/create/', views.BuyerCreateView.as_view(), name='buyer_create'),
    path('buyers/<int:pk>/edit/', views.BuyerUpdateView.as_view(), name='buyer_update'),

    # Товары
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),

    # Заказы (для админа)
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),

    # Отзывы
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
]