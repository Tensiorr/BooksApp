import uuid

from django.db import models


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=200, null=True)
    publication_date = models.DateField(null=True)
    isbn = models.CharField(max_length=100, unique=True)
    pages = models.PositiveIntegerField(null=True)
    cover = models.CharField(max_length=500, null=True)
    language = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.title
