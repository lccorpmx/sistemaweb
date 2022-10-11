from django.db import models
from django.conf import settings
# ...code

# Create your models here.
class Question(models.Model):
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', related_name='votes', on_delete=models.CASCADE)