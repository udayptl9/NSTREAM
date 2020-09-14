from django.db import models

class accounts(models.Model):
    email = models.CharField(max_length=250, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    age = models.CharField(max_length=10)
    mobileno = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=1000)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class password_verify_request(models.Model):
    email = models.CharField(max_length=250)
    token = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class GuestSettings(models.Model):
    timer = models.CharField(max_length=3, default='15')
    def __str__(self):
        return self.timer

class AdSettings(models.Model):
    ad_timing = models.CharField(max_length=5, default="900")
    def __str__(self):
        return self.ad_timing

class Page_settings(models.Model):
    per_page = models.CharField(max_length=3, default='12')
    def __str__(self):
        return self.per_page