from django.db import models

# Create your models here.

class Question(models.Model):
    description = models.TextField(blank=True)