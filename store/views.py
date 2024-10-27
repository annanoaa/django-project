from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from .models import Category, Product

class StoreHomeMixin:
    """
    Mixin to provide common functionality for store views.
    Includes methods for getting categories with product counts.
    """

    def get_categories_with_counts(self):
        """
        Returns all parent categories with their total product counts,
        including products from subcategories.
        """
        return Category.objects.filter(parent__isnull=True).annotate(
            product_count=Count('products', filter=Q(products__is_available=True)) +
                          Count('children__products', filter=Q(children__products__is_available=True))
        )


class StoreHomeView(StoreHomeMixin, ListView):
    """
    View for the store homepage.
    Displays featured products and main categories.
    """
    template_name = 'store/index.html'
    context_object_name = 'featured_products'

    def get_queryset(self):
        """
        Returns the first 6 available products as featured products.
        """
        return Product.objects.filter(is_available=True)[:6]

    def get_context_data(self, **kwargs):
        """
        Adds categories to the context.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_categories_with_counts()
        return context


class ShopView(StoreHomeMixin, ListView):
    """
    View for the shop page.
    Handles product filtering, searching, and pagination.
    """
    template_name = 'store/shop.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        """
        Returns filtered queryset based on category and search parameters.
        Handles both category filtering and search functionality.
        """
        queryset = Product.objects.filter(is_available=True)

        # Category filtering
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            subcategories = category.get_all_children()
            category_list = [category] + subcategories
            queryset = queryset.filter(categories__in=category_list).distinct()

        # Search filtering
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds additional context including categories, current category,
        total products count, and search query.
        """
        context = super().get_context_data(**kwargs)

        # Get current category if filtering by category
        category_slug = self.request.GET.get('category')
        current_category = None
        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)

        context.update({
            'categories': self.get_categories_with_counts(),
            'current_category': current_category,
            'total_products': Product.objects.filter(is_available=True).count(),
            'query': self.request.GET.get('q', '')
        })

        return context


class ProductDetailView(StoreHomeMixin, DetailView):
    """
    View for displaying product details.
    Includes related products and category sidebar.
    """
    model = Product
    template_name = 'store/shop-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """
        Returns queryset of only available products.
        """
        return super().get_queryset().filter(is_available=True)

    def get_context_data(self, **kwargs):
        """
        Adds related products and categories to the context.
        """
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Get related products
        related_products = Product.objects.filter(
            categories__in=product.categories.all(),
            is_available=True
        ).exclude(id=product.id).distinct()[:4]

        context.update({
            'related_products': related_products,
            'categories': self.get_categories_with_counts()
        })

        return context


class SearchView(ShopView):
    """
    View for handling product searches.
    Inherits from ShopView to maintain consistent filtering and pagination.
    """

    def get_queryset(self):
        """
        Returns search results or empty queryset if no query.
        """
        query = self.request.GET.get('q', '')
        if query:
            return super().get_queryset().filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()
        return Product.objects.none()


class ContactView(TemplateView):
    """
    View for displaying the contact page.
    Basic template rendering without form processing.
    """
    template_name = 'store/contact.html'

    def get_context_data(self, **kwargs):
        """
        Adds any additional context data needed for the contact page.
        Override this method to add more context data if needed.
        """
        context = super().get_context_data(**kwargs)

        return context