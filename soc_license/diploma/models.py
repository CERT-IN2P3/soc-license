from django.db import models


class Diploma(models.Model):
    uuid = models.CharField(max_length=100, primary_key=True)
    sha512sum = models.CharField(max_length=100)
