from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField

# Create your models here.

class DocDData(models.Model):
    id = models.AutoField(primary_key=True)
    junban = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    doc = models.TextField()
    book_id = models.CharField(max_length=100)
    search_vector = SearchVectorField(null=True)
    pages = models.TextField()
    
    class Meta(object):
        indexes = [GinIndex(fields=['search_vector'])]
        
    



    
