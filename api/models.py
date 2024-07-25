from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)

    def __str__(self):
        return self.title
class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
