from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import accounts

class emailverifyrequest(models.Model):
    email = models.EmailField(max_length=100)
    token = models.CharField(max_length=500)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class ads(models.Model):
    image = models.ImageField(upload_to='adimages')
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=250)
    user = models.ForeignKey(accounts, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class advideo(models.Model):
    video = models.FileField(upload_to='advideos')
    user = models.ForeignKey(accounts, on_delete=models.CASCADE)

    def __str__(self):
        return self.video.name

class theme(models.Model):
    is_dark = models.BooleanField(default=False)
    user = models.ForeignKey(accounts, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + " " + str(self.is_dark)
