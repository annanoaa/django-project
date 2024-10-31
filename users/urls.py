from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
]

# project/settings.py (add these settings)
AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    # ... other middleware ...
    'users.middleware.UserActivityMiddleware',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'