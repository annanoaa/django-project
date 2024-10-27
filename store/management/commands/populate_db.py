from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.db import transaction
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Deleting old data...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Create categories
        # self.stdout.write('Creating categories...')
        # categories = [
        #     Category.objects.create(name="Electronics"),
        #     Category.objects.create(name="Books"),
        #     Category.objects.create(name="Clothing"),
        #     Category.objects.create(name="Home & Kitchen"),
        #     Category.objects.create(name="Sports & Outdoors"),
        # ]
        #
        # # Create subcategories
        # electronics_subs = [
        #     Category.objects.create(name="Smartphones", parent=categories[0]),
        #     Category.objects.create(name="Laptops", parent=categories[0]),
        #     Category.objects.create(name="Accessories", parent=categories[0]),
        # ]
        #
        # books_subs = [
        #     Category.objects.create(name="Fiction", parent=categories[1]),
        #     Category.objects.create(name="Non-Fiction", parent=categories[1]),
        # ]
        #
        # # Create products
        # self.stdout.write('Creating products...')
        # products = [
        #     # Electronics
        #     Product.objects.create(name="iPhone 13", description="Latest iPhone model", price=999.99, quantity=50),
        #     Product.objects.create(name="Samsung Galaxy S21", description="Flagship Android phone", price=899.99,
        #                            quantity=40),
        #     Product.objects.create(name="MacBook Pro", description="Powerful laptop for professionals", price=1999.99,
        #                            quantity=25),
        #     Product.objects.create(name="Dell XPS 15", description="High-performance Windows laptop", price=1799.99,
        #                            quantity=30),
        #     Product.objects.create(name="AirPods Pro", description="Noise-cancelling earbuds", price=249.99,
        #                            quantity=100),
        #
        #     # Books
        #     Product.objects.create(name="The Great Gatsby", description="Classic novel by F. Scott Fitzgerald",
        #                            price=15.99, quantity=200),
        #     Product.objects.create(name="To Kill a Mockingbird", description="Harper Lee's masterpiece", price=14.99,
        #                            quantity=150),
        #     Product.objects.create(name="A Brief History of Time", description="Stephen Hawking's cosmology book",
        #                            price=18.99, quantity=75),
        #
        #     # Clothing
        #     Product.objects.create(name="Denim Jeans", description="Classic blue jeans", price=49.99, quantity=300),
        #     Product.objects.create(name="Cotton T-Shirt", description="Comfortable everyday tee", price=19.99,
        #                            quantity=500),
        #
        #     # Home & Kitchen
        #     Product.objects.create(name="Coffee Maker", description="Programmable drip coffee maker", price=79.99,
        #                            quantity=60),
        #     Product.objects.create(name="Microwave Oven", description="Countertop microwave", price=129.99,
        #                            quantity=40),
        #
        #     # Sports & Outdoors
        #     Product.objects.create(name="Yoga Mat", description="Non-slip exercise mat", price=29.99, quantity=150),
        #     Product.objects.create(name="Dumbbells Set", description="Adjustable weight set", price=199.99,
        #                            quantity=30),
        # ]
        #
        # # Assign categories to products
        # for product in products[:5]:
        #     product.categories.add(categories[0])
        #     product.categories.add(random.choice(electronics_subs))
        #
        # for product in products[5:8]:
        #     product.categories.add(categories[1])
        #     product.categories.add(random.choice(books_subs))
        #
        # for product in products[8:10]:
        #     product.categories.add(categories[2])
        #
        # for product in products[10:12]:
        #     product.categories.add(categories[3])
        #
        # for product in products[12:]:
        #     product.categories.add(categories[4])
        #
        # self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))