from django.db import models

from .common import *


class Post(models.Model):
    title = models.CharField(
        max_length=128
    )
    content = models.TextField(

    )

    def __str__(self):
        return f'{self.title}'
