from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Store URLs
    path('',
        views.StoreHomeView.as_view(),
        name='home'
    ),
    path('shop/',
        views.ShopView.as_view(),
        name='shop'
    ),
    path('search/',
        views.SearchView.as_view(),
        name='search'
    ),
    path('product/<slug:slug>/',
        views.ProductDetailView.as_view(),
        name='product_detail'
    ),
    path('contact/',
        views.ContactView.as_view(),
        name='contact'
    ),
]