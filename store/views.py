# store/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.shortcuts import render
from .models import Category, Product


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def index(request):
    return render(request, 'store/home.html')


def contact(request):
    return render(request, 'store/contact.html')


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/shop.html'
    paginate_by = 9

    def get_queryset(self):
        # Get the sort parameter from URL, default to '-created_at'
        sort_by = self.request.GET.get('sort', '-created_at')

        # Define allowed sort fields
        allowed_sort_fields = ['price', '-price', 'name', '-name', 'created_at', '-created_at']
        if sort_by not in allowed_sort_fields:
            sort_by = '-created_at'

        # Start with all products
        queryset = Product.objects.all()

        # Apply category filter if slug is present
        if self.kwargs.get('slug'):
            queryset = queryset.filter(category__slug=self.kwargs.get('slug'))

        # Apply sorting
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(product_count=Count('products'))
        context['get_elided_page_range'] = context['paginator'].get_elided_page_range(
            self.request.GET.get(self.page_kwarg, 1)
        )
        # Add current sort to context
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cache related products for this product
        cache_key = f'related_products_{self.object.id}'
        related_products = cache.get(cache_key)

        if not related_products:
            related_products = Product.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id)[:4]
            cache.set(cache_key, related_products, 60 * 30)  # Cache for 30 minutes

        context['related_products'] = related_products
        return context


def cart_processor(request):
    if hasattr(request, 'session'):
        cart = request.session.get('cart', {})
        return {'cart_count': len(cart)}
    return {'cart_count': 0}
