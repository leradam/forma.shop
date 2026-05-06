from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import ProductCategory, Buyer, Product, Order, Review
from .forms import ProductCategoryForm, BuyerForm, ProductForm, OrderForm, ReviewForm, RegistrationForm, CustomLoginForm

# --- Миксин для проверки, является ли пользователь администратором ---
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('app:home')  # или страница 403

# --- Главная страница ---
class HomeView(TemplateView):
    template_name = 'app/index.html'

# --- Категории (только просмотр для всех, редактирование – админу) ---
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'app/productcategory_list.html'
    context_object_name = 'categories'

class ProductCategoryDetailView(DetailView):
    model = ProductCategory
    template_name = 'app/productcategory_detail.html'
    context_object_name = 'category'

class ProductCategoryCreateView(AdminRequiredMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'app/productcategory_form.html'
    success_url = reverse_lazy('app:productcategory_list')

class ProductCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'app/productcategory_form.html'
    success_url = reverse_lazy('app:productcategory_list')

# --- Покупатели (только просмотр для всех, редактирование – админу) ---
class BuyerListView(ListView):
    model = Buyer
    template_name = 'app/buyer_list.html'
    context_object_name = 'buyers'

class BuyerDetailView(DetailView):
    model = Buyer
    template_name = 'app/buyer_detail.html'
    context_object_name = 'buyer'

class BuyerCreateView(AdminRequiredMixin, CreateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'app/buyer_form.html'
    success_url = reverse_lazy('app:buyer_list')

class BuyerUpdateView(AdminRequiredMixin, UpdateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'app/buyer_form.html'
    success_url = reverse_lazy('app:buyer_list')

# --- Товары (только просмотр для всех, редактирование – админу) ---
class ProductListView(ListView):
    model = Product
    template_name = 'app/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('app:product_list')

class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('app:product_list')

# --- Заказы (админ видит все, пользователь – только свои) ---
class OrderListView(ListView):
    model = Order
    template_name = 'app/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        # Для обычных пользователей – заказы, связанные с их профилем Buyer
        try:
            buyer = Buyer.objects.get(user=self.request.user)
            return Order.objects.filter(buyer=buyer)
        except Buyer.DoesNotExist:
            return Order.objects.none()

class OrderDetailView(DetailView):
    model = Order
    template_name = 'app/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        try:
            buyer = Buyer.objects.get(user=self.request.user)
            return Order.objects.filter(buyer=buyer)
        except Buyer.DoesNotExist:
            return Order.objects.none()

class OrderCreateView(AdminRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'app/order_form.html'
    success_url = reverse_lazy('app:order_list')

class OrderUpdateView(AdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'app/order_form.html'
    success_url = reverse_lazy('app:order_list')

# --- Отзывы (создавать может любой авторизованный, редактировать – админ) ---
class ReviewListView(ListView):
    model = Review
    template_name = 'app/review_list.html'
    context_object_name = 'reviews'

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'app/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'app/review_form.html'
    success_url = reverse_lazy('app:review_list')

    def form_valid(self, form):
        # Привязываем отзыв к текущему покупателю
        buyer, _ = Buyer.objects.get_or_create(user=self.request.user, defaults={
            'full_name': self.request.user.username,
            'email': self.request.user.email,
            'phone': '',
            'address': ''
        })
        form.instance.buyer = buyer
        return super().form_valid(form)

class ReviewUpdateView(AdminRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'app/review_form.html'
    success_url = reverse_lazy('app:review_list')

# --- Корзина и оформление (без изменений) ---
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('app:cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('app:cart_detail')

def cart_update(request, product_id, quantity):
    cart = request.session.get('cart', {})
    if int(quantity) <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = int(quantity)
    request.session['cart'] = cart
    return redirect('app:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        subtotal = product.price * qty
        total += subtotal
        products.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal
        })
    return render(request, 'app/cart_detail.html', {'cart_items': products, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('app:cart_detail')
    if request.method == 'POST':
        payment = request.POST.get('payment')
        delivery = request.POST.get('delivery_option')
        comment = request.POST.get('comment', '')
        buyer = Buyer.objects.get(user=request.user)
        order = Order.objects.create(
            buyer=buyer,
            payment=payment,
            delivery_option=delivery,
            registration_status='Оформлен',
            comment=comment
        )
        for product_id, qty in cart.items():
            product = Product.objects.get(id=int(product_id))
            order.products.add(product)
        order.save()
        request.session['cart'] = {}
        return redirect('app:order_detail', pk=order.id)
    return render(request, 'app/checkout.html')

@login_required
def my_orders(request):
    buyer = Buyer.objects.get(user=request.user)
    orders = Order.objects.filter(buyer=buyer).order_by('-date_of_creation')
    for order in orders:
        total = sum(product.price for product in order.products.all())
        order.total_price = total
    return render(request, 'app/my_orders.html', {'orders': orders})

# --- Регистрация и вход ---
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:home')
    else:
        form = RegistrationForm()
    return render(request, 'app/register.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'app/login.html'
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    return redirect('app:home')