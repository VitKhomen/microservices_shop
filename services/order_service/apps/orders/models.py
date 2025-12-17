from django.db import models
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user_id = models.IntegerField()  # ID користувача из user-service
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    user_email = models.EmailField(blank=True)  # Кеш email користувача
    user_name = models.CharField(max_length=200, blank=True)  # Кеш імені
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by User {self.user_id}"

    @property
    def item_count(self):
        '''Кількість товарів в замовленні'''
        return sum(item.quantity for item in self.items.all())

    @property
    def total_quantity(self):
        '''Загальна кількість товар'''
        return sum(item.quantity for item in self.items.all())

    def calculate_total(self):
        '''Перерахування сумми заказу'''
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = Decimal(total)
        return self.total_amount


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()  # ID товара з product-service
    product_name = models.CharField(max_length=200)  # Знимок назви товара
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # Ціна на час замовлення
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def subtotal(self):
        '''Підсума товару'''
        return self.price * self.quantity
