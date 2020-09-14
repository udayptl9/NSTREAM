from django.urls import path
from .import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home,name="home"),
    path('adImage/', views.adImage, name='adImage'),
    path('adVideo/', views.adVideo, name='adVideo'),
    path('delete_ad/<int:id>', views.deleteadImage, name='delete_adimage'),
    path('delete_adVideo/<int:id>', views.deleteadVideo, name='delete_advideo'),
    path('feedback/', views.feedback, name='feedback'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_email_check/<token>', views.verify_email_check, name='verify_email_check'),
]