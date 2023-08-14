from django.db import models


class Diploma(models.Model):
    uuid = models.CharField(max_length=100, primary_key=True)
    private_key = models.CharField(max_length=15000, default='')
    sha512sum = models.CharField(max_length=100)
