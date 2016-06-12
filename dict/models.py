from django.db import models


class Entry(models.Model):

    word = models.CharField(max_length=64, default=None)
    definition = models.CharField(max_length=250, default=None)
    response1 = models.CharField(max_length=64, default=None)
    response2 = models.CharField(max_length=64, default=None)
    queries = models.IntegerField(db_index=True, default=1)