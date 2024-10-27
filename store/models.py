from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            existing_slugs = Category.objects.filter(slug__startswith=base_slug).values_list('slug', flat=True)
            if not existing_slugs:
                self.slug = base_slug
            else:
                i = 1
                while f"{base_slug}-{i}" in existing_slugs:
                    i += 1
                self.slug = f"{base_slug}-{i}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_category_slug')
        ]

    def get_all_children(self):
        pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='static/img/')
    categories = models.ManyToManyField(Category, related_name='products')
    is_available = models.BooleanField(default=True)  # Make sure this field exists
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_total_price(self):
        return self.price