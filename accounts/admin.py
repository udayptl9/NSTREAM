from django.contrib import admin
from .models import accounts, password_verify_request, GuestSettings, AdSettings, Page_settings

admin.site.register(accounts)
admin.site.register(password_verify_request)
admin.site.register(GuestSettings)
admin.site.register(AdSettings)
admin.site.register(Page_settings)