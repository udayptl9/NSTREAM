from django.db import models
from accounts.models import accounts
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50)
    image = models.FileField(upload_to='subcategories')
    def __str__(self):
        return self.subcategory

class Language(models.Model):
    language = models.CharField(max_length=50)
    def __str__(self):
        return self.language

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    video = models.FileField(upload_to='uploads')
    posted_on = models.DateTimeField(default=timezone.now)
    video_ads = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(accounts, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.title)

class Upcoming(models.Model):
    title = models.CharField(max_length=250)
    thumbnail = models.FileField(upload_to='thumbnails')
    video = models.FileField(upload_to='trailers')
    
    def __str__(self):
        return self.title

class Notify(models.Model):
    email = models.EmailField(max_length=250)
    upcoming = models.ForeignKey(Upcoming, on_delete=models.CASCADE)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.email