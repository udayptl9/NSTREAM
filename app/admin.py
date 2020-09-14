from django.contrib import admin
from .models import emailverifyrequest, ads, advideo, theme

admin.site.register(emailverifyrequest)
admin.site.register(ads)
admin.site.register(advideo)
admin.site.register(theme)
admin.site.site_header = 'NSTREAM Administration'
