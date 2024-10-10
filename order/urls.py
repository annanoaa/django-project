# from django.urls import include, path
#
# urlpatterns = [
#     path('store/', include('store.urls')),
#     path('order/', include('order.urls')),  # this includes your order app's URLs
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_home, name='order_home'),
    path('history/', views.order_history, name='order_history'),
]
