from django.db import models

# Create your models here.
class Book(models.Model):
   book_title = models.CharField(max_length = 100)
   book_author = models.CharField(max_length = 100)
   book_img_url = models.CharField(max_length = 100)
   book_id = models.CharField(max_length = 100)
   book_recommender = models.CharField(max_length = 100)
