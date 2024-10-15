from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('categories/', views.all_categories, name='all_categories'),
    path('category/<int:category_id>/products/', views.category_products, name='category_products'),
    path('category/<int:category_id>/', views.category_products_page, name='category_products_page'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]