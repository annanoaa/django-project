from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from store.views import ProductListView, ProductDetailView
from order.views import CartListView, AddToCartView, CheckoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('users.urls', 'users'), namespace='users')),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_details'),
    path('category/', ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='product_list'),
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
