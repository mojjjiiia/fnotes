from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    subject = models.CharField(max_length=60)
    text = models.TextField()

    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.theme
