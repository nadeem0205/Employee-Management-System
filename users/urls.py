from django.urls import path
from . import views

urlpatterns = [
    # User registration endpoint
    path('register/', views.register, name='register'),

    # User login endpoint
    path('login/', views.user_login, name='login'),

    # User logout endpoint
    path('logout/', views.user_logout, name='logout'),
]
