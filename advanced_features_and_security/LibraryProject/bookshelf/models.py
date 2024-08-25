from django.db import models
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200,null= False, default= 'Unknown title')
    author = models.CharField(max_length=100, default='Unknown Author')
    publication_year = models.IntegerField(null= False, default=timezone.now())