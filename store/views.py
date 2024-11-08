from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .models import Category, Product


def handler404(request, exception):
    return render(request, '404.html', {
        'error_message': _('Page not found')
    }, status=404)


def handler500(request):
    return render(request, '500.html', {
        'error_message': _('Server error')
    }, status=500)


def index(request):
    return render(request, 'store/home.html', {
        'page_title': _('Welcome to our store')
    })


def contact(request):
    return render(request, 'store/contact.html', {
        'page_title': _('Contact Us'),
        'contact_info': {
            'address': _('123 Street, New York, USA'),
            'phone': _('Phone: +012 345 67890'),
            'email': _('Email: info@example.com')
        }
    })


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/shop.html'
    paginate_by = 9

    def get_queryset(self):
        # Get the current language
        current_language = get_language()

        # Get the sort parameter from URL, default to '-created_at'
        sort_by = self.request.GET.get('sort', '-created_at')

        # Define allowed sort fields with translations
        allowed_sort_fields = {
            'price': ('price', _('Price Low to High')),
            '-price': ('-price', _('Price High to Low')),
            'name': (f'name_{current_language}', _('Name A-Z')),
            '-name': (f'-name_{current_language}', _('Name Z-A')),
            'created_at': ('created_at', _('Oldest First')),
            '-created_at': ('-created_at', _('Newest First'))
        }

        # Get the actual sort field
        sort_field = allowed_sort_fields.get(sort_by, ('-created_at', _('Newest First')))[0]

        # Start with all products
        queryset = Product.objects.all()

        # Apply category filter if slug is present
        if self.kwargs.get('slug'):
            queryset = queryset.filter(category__slug=self.kwargs.get('slug'))

        # Apply sorting
        return queryset.order_by(sort_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get categories with translated names and product count
        context['categories'] = Category.objects.annotate(product_count=Count('products'))

        # Add pagination context
        context['get_elided_page_range'] = context['paginator'].get_elided_page_range(
            self.request.GET.get(self.page_kwarg, 1)
        )

        # Add current sort to context with translation
        current_sort = self.request.GET.get('sort', '-created_at')
        context['current_sort'] = current_sort

        # Add sorting options with translations
        context['sort_options'] = [
            {'value': 'price', 'label': _('Price Low to High')},
            {'value': '-price', 'label': _('Price High to Low')}
        ]

        # Add page title
        category_slug = self.kwargs.get('slug')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                context['page_title'] = _('Products in category: %(category)s') % {'category': category.name}
            except Category.DoesNotExist:
                context['page_title'] = _('All Products')
        else:
            context['page_title'] = _('All Products')

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cache related products for this product
        cache_key = f'related_products_{self.object.id}_{get_language()}'
        related_products = cache.get(cache_key)

        if not related_products:
            related_products = Product.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id)[:4]
            cache.set(cache_key, related_products, 60 * 30)  # Cache for 30 minutes

        context['related_products'] = related_products
        context['page_title'] = self.object.name
        context['product_details'] = {
            'category': _('Category'),
            'price': _('Price'),
            'in_stock': _('In Stock'),
            'out_of_stock': _('Out of Stock'),
            'description': _('Description')
        }
        return context


def cart_processor(request):
    if hasattr(request, 'session'):
        cart = request.session.get('cart', {})
        return {
            'cart_count': len(cart),
            'cart_label': _('Cart')
        }
    return {
        'cart_count': 0,
        'cart_label': _('Cart')
    }