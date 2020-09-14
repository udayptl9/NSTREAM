from django.urls import path
from . import views

urlpatterns = [
    path('', views.subadmin_view, name='subadmin_view'),
    path('add/', views.subdomain_add, name='subadmin_add'),
    path('<int:subadminid>/', views.subadmin_detail, name='subadmin_detail'),
    path('delete/<int:id>', views.subadmin_delete, name='subadmin_delete'),
]