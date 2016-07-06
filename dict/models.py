from django.db import models


class Entry(models.Model):

    word = models.CharField(max_length=64, default=None)
    definition = models.CharField(max_length=1000, default=None)
    translation = models.CharField(max_length=1000, default=None, blank=True, null=True)
    response1 = models.CharField(max_length=64, default=None)
    response2 = models.CharField(max_length=64, default=None)
    queries = models.IntegerField(db_index=True, default=1)


class Token(models.Model):

    token = models.CharField(max_length=500, default=None)
    created = models.DateTimeField(auto_now_add=True)