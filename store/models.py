from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='No description available')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)  # Add this line
    categories = models.ManyToManyField('Category', related_name='products')
    image = models.ImageField(upload_to='products/', default='products/default.jpg')

    @property
    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name
