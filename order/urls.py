from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    # Order URLs
    path('cart/',
        views.OrderCartView.as_view(),
        name='cart_detail'
    ),
    path('add-to-cart/<int:product_id>/',
        views.AddToCartView.as_view(),
        name='add_to_cart'
    ),
    path('remove-from-cart/<int:item_id>/',
        views.RemoveFromCartView.as_view(),
        name='remove_from_cart'
    ),
    path('checkout/',
        views.CheckoutView.as_view(),
        name='checkout'
    ),
]