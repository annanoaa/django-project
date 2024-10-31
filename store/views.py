from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Category, Product
from django.shortcuts import render


def index(request):
    return render(request, 'store/index.html')


def contact(request):
    return render(request, 'store/contact.html')


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/shop.html'
    paginate_by = 9

    def get_queryset(self):
        if self.kwargs.get('slug'):
            category = Category.objects.filter(slug=self.kwargs.get('slug')).first()
            return Product.objects.filter(category=category)
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(product_count=Count('products'))
        context['get_elided_page_range'] = context['paginator'].get_elided_page_range(self.request.GET.get(self.page_kwarg, 1))

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=self.object.category)
        return context
