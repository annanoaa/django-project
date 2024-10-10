from django.urls import path
from store import views

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('categories/', views.all_categories, name='all_categories'),
    path('products/', views.products_with_categories, name='products_with_categories'),
]
