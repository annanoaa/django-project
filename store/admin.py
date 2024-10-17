from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'get_products_count')
    list_filter = ('parent',)
    search_fields = ('name',)

    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = 'Products Count'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'get_categories')
    list_filter = ('categories',)
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'