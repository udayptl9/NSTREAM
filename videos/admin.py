from django.contrib import admin
from .models import Category, Language,  Video, Subcategory, Notify, Upcoming

admin.site.register(Video)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Notify)
admin.site.register(Upcoming)