from django.db import models
from django.utils import timezone

class Subadmin(models.Model):
    email = models.EmailField()
    superuser = models.BooleanField(default=False)
    addvideo = models.BooleanField(default=False)
    addcategory = models.BooleanField(default=False)
    addlanguage = models.BooleanField(default=False)
    added_on = models.DateTimeField(default=timezone.now)
    joined = models.BooleanField(default=False)