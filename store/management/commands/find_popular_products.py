from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from order.models import CartItem, Cart
from store.models import Product


class Command(BaseCommand):
    help = 'Find the three most popular products in users\' carts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--show-count',
            action='store_true',
            help=_('Show the number of carts for each product')
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(_('Finding most popular products...')))

        # Get all products in carts with their cart count
        popular_products = Product.objects.filter(
            cartitem__cart__isnull=False  # Only include products that are in carts
        ).annotate(
            cart_count=Count('cartitem__cart', distinct=True)  # Count unique carts
        ).order_by(
            '-cart_count'  # Order by number of carts, descending
        )[:3]  # Get top 3

        if not popular_products:
            self.stdout.write(self.style.WARNING(_('No products found in any carts.')))
            return

        # Print results
        self.stdout.write(self.style.SUCCESS('\n' + _('Top 3 most popular products:') + '\n'))

        for index, product in enumerate(popular_products, 1):
            # Get basic product info
            product_info = f"{index}. {product.name}"

            # Add cart count if requested
            if options['show_count']:
                cart_count = product.cart_count
                cart_text = _('cart') if cart_count == 1 else _('carts')
                product_info += f" ({cart_count} {cart_text})"

            # Add price
            product_info += f" - {product.price} USD"

            # Get categories
            categories = ", ".join([cat.name for cat in product.category.all()])
            if categories:
                product_info += f" [{categories}]"

            # Style and print the line
            if index == 1:
                self.stdout.write(self.style.SUCCESS(product_info))
            elif index == 2:
                self.stdout.write(self.style.WARNING(product_info))
            else:
                self.stdout.write(self.style.HTTP_INFO(product_info))

        # Print summary
        total_carts = Cart.objects.count()
        total_products = Product.objects.count()

        self.stdout.write('\n' + self.style.SUCCESS(_('Summary:')))
        self.stdout.write(_('Total number of carts: %(cart_count)s') % {'cart_count': total_carts})
        self.stdout.write(_('Total number of products: %(product_count)s') % {'product_count': total_products})

    def get_cart_percentage(self, cart_count, total_carts):
        """Calculate percentage of carts containing a product"""
        if total_carts == 0:
            return 0
        return (cart_count / total_carts) * 100