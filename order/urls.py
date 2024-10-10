from django.urls import path
from order import views

urlpatterns = [
    path('', views.order_home, name='order_home'),
    path('status/', views.order_status, name='order_status'),
]
