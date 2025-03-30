from django.contrib import admin
from .models import Item, Product

# Настройки для модели Item
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'emailAdress', 'phoneNumber']
    search_fields = ['name', 'emailAdress']

# Настройки для модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available']
    list_filter = ['available']
    search_fields = ['name']