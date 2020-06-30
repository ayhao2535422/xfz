from django.db import models


class PayInfo(models.Model):
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    path = models.FilePathField()