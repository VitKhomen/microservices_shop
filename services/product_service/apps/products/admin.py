from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def product_count(self, obj):
        count = obj.products.filter(is_active=True).count()
        return format_html('<strong>{}</strong>', count)
    product_count.short_description = 'Активних продуктів'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview', 'name', 'category', 'price', 'stock_quantity',
        'stock_status', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'stock_quantity']
    list_per_page = 25

    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image_url
            )
        return format_html('<span style="color: gray;">Немає зображення</span>')
    image_preview.short_description = 'Зображення'

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'description', 'category')
        }),
        ('Ціна та наявність', {
            'fields': ('price', 'stock_quantity', 'is_active')
        }),
        ('Зображення', {
            'fields': ('image_url', 'image_display')
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'image_display']

    def image_display(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px;" />',
                obj.image_url
            )
        return 'Зображення не завантажено'
    image_display.short_description = 'Попередній перегляд'

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            color = 'red'
            text = 'Немає в наявності'
        elif obj.stock_quantity < 10:
            color = 'orange'
            text = 'Мало'
        else:
            color = 'green'
            text = 'В наявності'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )
    stock_status.short_description = 'Статус'

    actions = ['mark_as_active', 'mark_as_inactive', 'reset_stock']

    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} продуктів активовано.')
    mark_as_active.short_description = 'Активувати вибрані продукти'

    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} продуктів деактивовано.')
    mark_as_inactive.short_description = 'Деактивувати вибрані продукти'

    def reset_stock(self, request, queryset):
        updated = queryset.update(stock_quantity=0)
        self.message_user(
            request, f'Кількість скинута для {updated} продуктів.')
    reset_stock.short_description = 'Скинути кількість до 0'
