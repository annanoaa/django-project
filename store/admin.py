from django.contrib import admin
from store.models import Product, Category


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug', 'created_at')


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'updated_at', 'image')
