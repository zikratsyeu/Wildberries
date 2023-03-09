from django.db import models

# Create your models here.
from django.db import models


class WildberriesProduct(models.Model):
    article = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
