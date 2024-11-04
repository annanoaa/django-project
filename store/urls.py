from django.urls import path
from store import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact')
]

