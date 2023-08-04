from django.db import models


class Lang(models.Model):
    """
    A class to handle multi-lang support
    """
    short = models.CharField(max_length=2, primary_key=True)
    long = models.CharField(max_length=20)
