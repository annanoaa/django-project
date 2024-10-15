from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product
from django.db.models import Count, Sum, F, Max, Min, Avg, Q


def store_home(request):
    return render(request, 'store_home.html')

def all_categories(request):
    categories = Category.objects.filter(parent__isnull=True).annotate(
        product_count=Count('products', distinct=True) +
                      Count('children__products', distinct=True) +
                      Count('children__children__products', distinct=True)
    ).values('id', 'name', 'product_count')
    return JsonResponse(list(categories), safe=False)

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(categories=category)

    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    stats = products.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price'),
        total_value=Sum(F('price') * F('quantity'))
    )

    context = {
        'category': category,
        'products': page_obj,
        'stats': stats,
    }
    return render(request, 'category_products.html', context)
def category_products_page(request, category_id):
    return render(request, 'category_products.html', {'category_id': category_id})

def product_detail(request, product_id):
    # product = get_object_or_404(Product, id=product_id)
    # data = {
    #     'id': product.id,
    #     'name': product.name,
    #     'description': product.description,
    #     'price': float(product.price),
    #     'quantity': product.quantity,
    #     'categories': list(product.categories.values_list('name', flat=True)),
    #     'image_url': product.image.url if product.image else None
    # }
    # return JsonResponse(data)

    product = get_object_or_404(Product, id=product_id)
    total_value = product.price * product.quantity
    context = {
        'product': product,
        'total_value': total_value,
    }
    return render(request, 'product_detail.html', {'product': product})
