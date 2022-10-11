from django.db import models
from django.conf import settings
# Create your models here.
class Answer(models.Model):
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)


