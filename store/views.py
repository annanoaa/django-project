from django.http import JsonResponse
from .models import Category, Product
from django.http import HttpResponse

def store_home(request):
    return HttpResponse("Welcome to the Store Home!")

def all_categories(request):
    categories = Category.objects.all().values('id', 'name', 'parent__name')
    return JsonResponse(list(categories), safe=False)


def products_with_categories(request):
    products = Product.objects.all()

    result = []
    for product in products:
        categories = product.categories.values_list('name', flat=True)  # Get category names as a list
        result.append({
            'id': product.id,
            'name': product.name,
            'categories': list(categories)
        })

    return JsonResponse(result, safe=False)