from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login2'),
    path('logout/', views.logout, name='logout2'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_verify/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_sent/', views.password_reset_sent, name='password_reset_sent'),
    path('guest_login/', views.guest_login, name='guest_login'),
    path('settings/', views.guest_settings, name='guest_settings'),
]