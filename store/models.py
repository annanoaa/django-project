# from django.db import models
# from django.utils.text import slugify
# from django.core.cache import cache
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(blank=True)
#
#     class Meta:
#         ordering = ['name']  # Add default ordering for categories
#         verbose_name_plural = 'Categories'
#
#     def save(self, *args, **kwargs):
#         # Generate slug combining ID and name
#         if not self.slug and self.id is not None:
#             self.slug = f"{self.id}-{slugify(self.name)}"
#
#         # Clear category cache when saving
#         cache.delete('all_categories')
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def product_count(self):
#         return self.products.count()
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(
#         Category,
#         related_name='products',
#         on_delete=models.CASCADE,
#         blank=False
#     )
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=False,
#         db_index=True  # Add index for price sorting
#     )
#     stock = models.PositiveIntegerField(default=0, blank=False)
#     image = models.ImageField(upload_to='products/', blank=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(unique=True, blank=True)
#
#     class Meta:
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['created_at']),
#             models.Index(fields=['name']),  # Add index for name sorting
#             models.Index(fields=['category', 'created_at']),  # Compound index for category filtering
#         ]
#
#     def save(self, *args, **kwargs):
#         if not self.slug and self.id is not None:
#             self.slug = f"{self.id}-{slugify(self.name)}"
#
#         # Clear related caches
#         cache.delete(f'product_details_{self.id}')
#         cache.delete(f'related_products_{self.id}')
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def is_in_stock(self):
#         return self.stock > 0
#
#     def get_related_products(self):
#         """Get related products from the same category"""
#         return Product.objects.filter(
#             category=self.category
#         ).exclude(id=self.id)[:4]

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        # Generate slug combining ID and name
        if not self.slug and self.id is not None:
            self.slug = f"{self.id}-{slugify(self.name)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    stock = models.PositiveIntegerField(default=0, blank=False)
    image = models.ImageField(upload_to='products/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.id is not None:
            self.slug = f"{self.id}-{slugify(self.name)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
