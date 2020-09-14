from django.urls import path
from . import views

urlpatterns = [
    path('upcoming/', views.upcoming_trailer, name='upcoming'),
    path('upcoming/<id>', views.upcoming_view, name='upcoming_view'),
    path('video_add/', views.video_add, name='video_add'),
    path('video_manage/', views.video_manage, name='video_manage'),
    path('category_add/', views.category_add, name='category_add'),
    path('subcategory_add/', views.subcategory_add, name='subcategory_add'),
    path('langauge_add/', views.language_add, name='language_add'),
    path('video_view/<id>/', views.video_view, name='video_view' ),
    path('video_update/<id>/', views.video_update, name='video_update'),
    path('video_delete/<id>/', views.video_delete, name='video_delete'),
    path('video_ads/<id>/', views.video_ads, name='video_ads'),
    path('<category>/', views.view_all, name='view_all'),
    path('<category>/<subcategory>/', views.sub_view_all, name='sub_view_all'),
]